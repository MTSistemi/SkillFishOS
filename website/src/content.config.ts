import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Italian documentation, authored as Markdown in src/content/docs/.
const docs = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/docs' }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    group: z.string().default('Generale'),
    order: z.number().default(99),
  }),
});

export const collections = { docs };
