<<<<<<< HEAD
﻿import { defineConfig, globalIgnores } from "eslint/config";
=======
import { defineConfig, globalIgnores } from "eslint/config";
>>>>>>> e46fdbbaf44880c2cb0f4e0fb06bafc7d464da49
import nextVitals from "eslint-config-next/core-web-vitals";
import nextTs from "eslint-config-next/typescript";

const eslintConfig = defineConfig([
  ...nextVitals,
  ...nextTs,
  // Override default ignores of eslint-config-next.
  globalIgnores([
    // Default ignores of eslint-config-next:
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
  ]),
]);

export default eslintConfig;
