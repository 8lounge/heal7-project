import * as React from 'react';
import { cn } from '@/lib/utils';

interface ProgressProps {
  value?: number;
  max?: number;
  className?: string;
  showText?: boolean;
  color?: 'default' | 'purple' | 'blue' | 'green' | 'red';
}

const Progress = React.forwardRef<HTMLDivElement, ProgressProps>(
  ({ value = 0, max = 100, className, showText = true, color = 'default', ...props }, ref) => {
    const percentage = Math.min(100, Math.max(0, (value / max) * 100));
    
    const colorClasses = {
      default: 'bg-purple-500',
      purple: 'bg-purple-500',
      blue: 'bg-blue-500',
      green: 'bg-green-500',
      red: 'bg-red-500',
    };

    return (
      <div
        ref={ref}
        className={cn('relative w-full', className)}
        {...props}
      >
        <div className="h-2 w-full bg-slate-700/50 rounded-full overflow-hidden">
          <div
            className={cn(
              'h-full transition-all duration-300 ease-out',
              colorClasses[color]
            )}
            style={{ width: `${percentage}%` }}
          />
        </div>
        {showText && (
          <div className="mt-1 text-right text-xs text-slate-400">
            {Math.round(percentage)}%
          </div>
        )}
      </div>
    );
  }
);
Progress.displayName = 'Progress';

export { Progress };