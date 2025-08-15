import React from 'react';
import { motion } from 'framer-motion';

interface SubPageHeroProps {
  title: React.ReactNode;
  subtitle: string;
  backgroundImage: string;
}

export const SubPageHero: React.FC<SubPageHeroProps> = ({ title, subtitle, backgroundImage }) => {
  const heroStyle = {
    backgroundImage: `url(${backgroundImage})`,
  };

  return (
    <section className="relative h-[240px] flex items-center justify-center text-white bg-cover bg-center" style={heroStyle}>
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" />
      <div className="container mx-auto px-4 text-center relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="max-w-3xl mx-auto"
        >
          <h1 className="heading-lg text-white mb-4">{title}</h1>
          <p className="text-xl text-slate-300">{subtitle}</p>
        </motion.div>
      </div>
    </section>
  );
};