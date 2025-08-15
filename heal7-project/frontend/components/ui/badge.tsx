import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const badgeVariants = cva(
  'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        default:
          'border-transparent bg-primary text-primary-foreground hover:bg-primary/80',
        secondary:
          'border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80',
        destructive:
          'border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80',
        outline: 'text-foreground',
        // 오행 색상
        wood: 'border-green-500/20 bg-green-500/10 text-green-400',
        fire: 'border-red-500/20 bg-red-500/10 text-red-400',
        earth: 'border-yellow-500/20 bg-yellow-500/10 text-yellow-400',
        metal: 'border-slate-400/20 bg-slate-500/10 text-slate-300',
        water: 'border-blue-500/20 bg-blue-500/10 text-blue-400',
        // 십신 색상
        bigeop: 'border-violet-500/20 bg-violet-500/10 text-violet-400',
        siksang: 'border-cyan-500/20 bg-cyan-500/10 text-cyan-400',
        jaeseong: 'border-emerald-500/20 bg-emerald-500/10 text-emerald-400',
        gwansal: 'border-amber-500/20 bg-amber-500/10 text-amber-400',
        inseong: 'border-pink-500/20 bg-pink-500/10 text-pink-400',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}

export { Badge, badgeVariants };