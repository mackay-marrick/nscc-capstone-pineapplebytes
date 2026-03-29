<<<<<<< HEAD
﻿import type { Config } from "tailwindcss";
=======
import type { Config } from "tailwindcss";
>>>>>>> e46fdbbaf44880c2cb0f4e0fb06bafc7d464da49

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
      },
    },
  },
  plugins: [],
};
<<<<<<< HEAD
export default config;
=======
export default config;
>>>>>>> e46fdbbaf44880c2cb0f4e0fb06bafc7d464da49
