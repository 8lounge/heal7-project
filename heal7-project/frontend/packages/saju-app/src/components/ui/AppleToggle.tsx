import React from 'react';
import { motion } from 'framer-motion';

interface AppleToggleProps {
  isOn: boolean;
  onToggle: () => void;
  leftIcon?: string;
  rightIcon?: string;
  leftLabel?: string;
  rightLabel?: string;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  disabled?: boolean;
}

const AppleToggle: React.FC<AppleToggleProps> = ({
  isOn,
  onToggle,
  leftIcon = '☀️',
  rightIcon = '🌙', 
  leftLabel = '낮',
  rightLabel = '밤',
  size = 'md',
  className = '',
  disabled = false
}) => {
  // Size configurations
  const sizeConfig = {
    sm: {
      track: 'w-10 h-6',
      thumb: 'w-4 h-4',
      thumbActive: 'w-5 h-5',
      text: 'text-xs',
      spacing: 'gap-2',
      iconSize: 'text-sm',
      padding: 'px-2 py-1',
    },
    md: {
      track: 'w-14 h-8', 
      thumb: 'w-6 h-6',
      thumbActive: 'w-7 h-7',
      text: 'text-sm',
      spacing: 'gap-3',
      iconSize: 'text-base',
      padding: 'px-3 py-2',
    },
    lg: {
      track: 'w-16 h-10',
      thumb: 'w-8 h-8',
      thumbActive: 'w-9 h-9', 
      text: 'text-base',
      spacing: 'gap-4',
      iconSize: 'text-lg',
      padding: 'px-4 py-3',
    }
  };

  const config = sizeConfig[size];

  return (
    <div className={`flex items-center ${config.spacing} ${className}`}>
      {/* Left Label & Icon */}
      <div className={`flex items-center gap-1 transition-all duration-300 ${
        !isOn 
          ? 'text-blue-600 drop-shadow-sm' 
          : 'text-gray-400 opacity-60'
      }`}>
        <span className={config.iconSize}>{leftIcon}</span>
        <span className={`${config.text} font-medium`}>{leftLabel}</span>
      </div>

      {/* Apple-style Toggle Track */}
      <motion.button
        onClick={disabled ? undefined : onToggle}
        disabled={disabled}
        className={`
          ${config.track} 
          relative rounded-full 
          transition-all duration-300 ease-out
          focus:outline-none focus:ring-4 focus:ring-opacity-30
          ${disabled ? 'cursor-not-allowed opacity-50' : 'cursor-pointer'}
          ${isOn 
            ? 'bg-gradient-to-r from-indigo-500 to-purple-600 shadow-lg focus:ring-purple-300' 
            : 'bg-gradient-to-r from-blue-500 to-blue-600 shadow-lg focus:ring-blue-300'
          }
        `}
        whileTap={disabled ? {} : { scale: 0.95 }}
        animate={{
          boxShadow: isOn 
            ? '0 4px 20px rgba(99, 102, 241, 0.4), 0 2px 8px rgba(79, 70, 229, 0.3)'
            : '0 4px 20px rgba(59, 130, 246, 0.4), 0 2px 8px rgba(37, 99, 235, 0.3)'
        }}
      >
        {/* Animated Thumb */}
        <motion.div
          className={`
            absolute top-1 
            bg-white rounded-full 
            shadow-lg border border-white/20
            flex items-center justify-center
            backdrop-blur-sm
          `}
          animate={{
            left: isOn ? 'calc(100% - 1.75rem)' : '0.25rem',
            width: isOn ? config.thumbActive : config.thumb,
            height: isOn ? config.thumbActive : config.thumb,
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15), 0 1px 4px rgba(0, 0, 0, 0.1)'
          }}
          transition={{
            type: 'spring',
            stiffness: 500,
            damping: 30,
            mass: 1
          }}
        >
          <span className={`${config.iconSize} transition-transform duration-200 ${
            !isOn ? 'scale-100' : 'scale-90'
          }`}>
            {isOn ? rightIcon : leftIcon}
          </span>
        </motion.div>

        {/* Subtle Inner Glow */}
        <div className={`
          absolute inset-0 rounded-full
          ${isOn 
            ? 'bg-gradient-to-r from-indigo-400/20 to-purple-500/20' 
            : 'bg-gradient-to-r from-blue-400/20 to-blue-500/20'
          }
        `} />
      </motion.button>

      {/* Right Label & Icon */}
      <div className={`flex items-center gap-1 transition-all duration-300 ${
        isOn 
          ? 'text-purple-600 drop-shadow-sm' 
          : 'text-gray-400 opacity-60'
      }`}>
        <span className={config.iconSize}>{rightIcon}</span>
        <span className={`${config.text} font-medium`}>{rightLabel}</span>
      </div>
    </div>
  );
};

export default AppleToggle;