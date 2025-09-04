#!/bin/bash
#
# SSL Certificate Auto-Renewal Script for HEAL7 Services
# Created: 2025-09-03
# Purpose: Automatically renew Let's Encrypt certificates 30 days before expiry
#
# This script:
# 1. Checks all certificates for expiry within 30 days
# 2. Attempts renewal for certificates that need it
# 3. Reloads nginx if any certificates were renewed
# 4. Sends notifications about renewal status
# 5. Logs all activities
#

# Configuration
LOG_FILE="/var/log/ssl-renewal.log"
NOTIFICATION_EMAIL="arne40@heal7.com"
RENEWAL_DAYS=30
NGINX_CONFIG_TEST_CMD="nginx -t"
NGINX_RELOAD_CMD="systemctl reload nginx"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to log messages
log_message() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"
}

# Function to send notification
send_notification() {
    local subject="$1"
    local body="$2"
    
    # Log the notification
    log_message "INFO" "Notification: $subject"
    
    # Try to send email if mail command is available
    if command -v mail >/dev/null 2>&1; then
        echo "$body" | mail -s "$subject" "$NOTIFICATION_EMAIL" 2>/dev/null
    fi
    
    # Also log to syslog for system monitoring
    logger -t ssl-renewal "$subject: $body"
}

# Function to get certificate expiry date in seconds since epoch
get_cert_expiry_seconds() {
    local cert_path="$1"
    openssl x509 -in "$cert_path" -noout -enddate | cut -d= -f2 | xargs -I {} date -d {} +%s 2>/dev/null
}

# Function to get certificate domains
get_cert_domains() {
    local cert_path="$1"
    openssl x509 -in "$cert_path" -noout -text | grep -A1 "Subject Alternative Name" | tail -1 | sed 's/DNS://g' | sed 's/, / /g' | xargs || echo "unknown"
}

# Function to check and renew certificates
check_and_renew_certificates() {
    local renewed_count=0
    local failed_count=0
    local checked_count=0
    local renewal_log=""
    
    log_message "INFO" "Starting SSL certificate check and renewal process..."
    
    # Get current timestamp
    local current_time=$(date +%s)
    local renewal_threshold=$((current_time + (RENEWAL_DAYS * 24 * 3600)))
    
    # Check each certificate
    while IFS= read -r cert_line; do
        if [[ $cert_line =~ ^[[:space:]]*Certificate[[:space:]]+Name:[[:space:]]+(.+)$ ]]; then
            local cert_name="${BASH_REMATCH[1]}"
            checked_count=$((checked_count + 1))
            
            log_message "INFO" "Checking certificate: $cert_name"
            
            # Get certificate details using certbot
            local cert_info=$(certbot certificates -d "$cert_name" 2>/dev/null | grep -A10 "Certificate Name: $cert_name")
            
            # Extract expiry date
            local expiry_line=$(echo "$cert_info" | grep "Expiry Date:")
            if [[ $expiry_line =~ ([0-9]{4}-[0-9]{2}-[0-9]{2}[[:space:]]+[0-9]{2}:[0-9]{2}:[0-9]{2}) ]]; then
                local expiry_date="${BASH_REMATCH[1]}"
                local expiry_seconds=$(date -d "$expiry_date" +%s 2>/dev/null)
                
                if [ -z "$expiry_seconds" ]; then
                    log_message "WARN" "Could not parse expiry date for $cert_name: $expiry_date"
                    continue
                fi
                
                local days_until_expiry=$(( (expiry_seconds - current_time) / 86400 ))
                
                log_message "INFO" "$cert_name expires in $days_until_expiry days ($expiry_date)"
                
                # Check if renewal is needed
                if [ $expiry_seconds -le $renewal_threshold ]; then
                    log_message "WARN" "$cert_name needs renewal (expires in $days_until_expiry days)"
                    
                    # Attempt renewal
                    log_message "INFO" "Starting renewal for $cert_name..."
                    
                    if certbot renew --cert-name "$cert_name" --quiet --no-random-sleep-on-renew; then
                        log_message "SUCCESS" "Successfully renewed certificate: $cert_name"
                        renewed_count=$((renewed_count + 1))
                        renewal_log="$renewal_log\n✅ $cert_name (was expiring in $days_until_expiry days)"
                    else
                        log_message "ERROR" "Failed to renew certificate: $cert_name"
                        failed_count=$((failed_count + 1))
                        renewal_log="$renewal_log\n❌ $cert_name (FAILED - manual intervention required)"
                    fi
                else
                    log_message "INFO" "$cert_name is valid for $days_until_expiry days, no renewal needed"
                fi
            else
                log_message "WARN" "Could not extract expiry date for $cert_name"
            fi
        fi
    done < <(certbot certificates 2>/dev/null)
    
    # Summary
    log_message "INFO" "Certificate check completed: $checked_count checked, $renewed_count renewed, $failed_count failed"
    
    # Reload nginx if any certificates were renewed
    if [ $renewed_count -gt 0 ]; then
        log_message "INFO" "Reloading nginx configuration..."
        
        # Test nginx configuration first
        if $NGINX_CONFIG_TEST_CMD >/dev/null 2>&1; then
            if $NGINX_RELOAD_CMD; then
                log_message "SUCCESS" "Nginx reloaded successfully"
                
                # Send success notification
                send_notification "SSL Certificates Renewed Successfully" \
                    "HEAL7 SSL Certificate Renewal Report

✅ RENEWAL SUCCESSFUL

Certificates renewed: $renewed_count
Certificates failed: $failed_count
Total certificates checked: $checked_count

Details:$renewal_log

Nginx has been reloaded successfully.

Server: $(hostname)
Date: $(date)
Log file: $LOG_FILE"
                
            else
                log_message "ERROR" "Failed to reload nginx after certificate renewal"
                failed_count=$((failed_count + 1))
            fi
        else
            log_message "ERROR" "Nginx configuration test failed, not reloading"
            failed_count=$((failed_count + 1))
        fi
    fi
    
    # Send notification if there were failures
    if [ $failed_count -gt 0 ]; then
        send_notification "SSL Certificate Renewal Issues Detected" \
            "HEAL7 SSL Certificate Renewal Report

⚠️ ISSUES DETECTED

Certificates renewed: $renewed_count
Certificates failed: $failed_count
Total certificates checked: $checked_count

Details:$renewal_log

Please check the server and renew failed certificates manually.

Server: $(hostname)
Date: $(date)
Log file: $LOG_FILE"
    fi
    
    # Return status
    return $failed_count
}

# Function to show help
show_help() {
    echo "HEAL7 SSL Certificate Auto-Renewal Script"
    echo
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  --check-only    Only check certificate expiry dates, don't renew"
    echo "  --force         Force renewal even if not within $RENEWAL_DAYS days"
    echo "  --dry-run       Perform a dry run (test mode)"
    echo "  --help          Show this help message"
    echo
    echo "Examples:"
    echo "  $0                    # Normal operation: check and renew if needed"
    echo "  $0 --check-only      # Just check expiry dates"
    echo "  $0 --dry-run         # Test renewal without actually renewing"
    echo
}

# Main execution
main() {
    local check_only=false
    local force_renewal=false
    local dry_run=false
    
    # Parse command line arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --check-only)
                check_only=true
                shift
                ;;
            --force)
                force_renewal=true
                RENEWAL_DAYS=0
                shift
                ;;
            --dry-run)
                dry_run=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                log_message "ERROR" "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Create log directory if it doesn't exist
    mkdir -p "$(dirname "$LOG_FILE")"
    
    # Start logging
    log_message "INFO" "=== HEAL7 SSL Certificate Renewal Process Started ==="
    log_message "INFO" "Hostname: $(hostname)"
    log_message "INFO" "Date: $(date)"
    log_message "INFO" "User: $(whoami)"
    log_message "INFO" "Renewal threshold: $RENEWAL_DAYS days"
    
    if [ "$dry_run" = true ]; then
        log_message "INFO" "Running in DRY RUN mode"
    fi
    
    # Check if running as root
    if [ "$EUID" -ne 0 ]; then
        log_message "ERROR" "This script must be run as root (use sudo)"
        exit 1
    fi
    
    # Check if certbot is available
    if ! command -v certbot >/dev/null 2>&1; then
        log_message "ERROR" "certbot command not found. Please install certbot first."
        exit 1
    fi
    
    # Check only mode
    if [ "$check_only" = true ]; then
        log_message "INFO" "Running in CHECK ONLY mode"
        certbot certificates
        exit 0
    fi
    
    # Main certificate check and renewal
    if [ "$dry_run" = true ]; then
        log_message "INFO" "Performing dry run renewal check..."
        certbot renew --dry-run
    else
        check_and_renew_certificates
    fi
    
    local exit_code=$?
    
    log_message "INFO" "=== HEAL7 SSL Certificate Renewal Process Completed ==="
    
    exit $exit_code
}

# Execute main function with all arguments
main "$@"