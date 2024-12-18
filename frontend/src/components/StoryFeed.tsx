'use client'

import Link from 'next/link'
import { useState } from 'react'

interface Chapter {
  id: number
  title: string
  summary: string
  slug: string
  date: string
}

export default function StoryFeed() {
  const [chapters] = useState<Chapter[]>([
    {
      id: 1,
      title: "The Awakening",
      summary: "In the shadow of forgotten titans, a lone traveler discovers an ancient secret that will change everything...",
      slug: "chapter-1-the-awakening",
      date: "2024-03-18"
    },
    {
      id: 2,
      title: "Echoes of the Giants",
      summary: "As the truth about the ancient civilization emerges, our heroes face an impossible choice...",
      slug: "chapter-2-echoes-of-giants",
      date: "2024-03-19"
    }
  ])

  return (
    <section id="story" className="space-y-8">
      <h2 className="text-xl font-bold text-green-500">&gt; Story_Archives</h2>
      <div className="border border-green-500 rounded-lg overflow-hidden">
        <div className="bg-gray-800 text-green-400 px-4 py-2 font-bold">
          &gt; Generated Chapters
        </div>
        <div className="bg-black p-4 divide-y divide-green-500/20">
          {chapters.map((chapter) => (
            <Link 
              key={chapter.id}
              href={`/chapters/${chapter.slug}`}
              className="block p-4 hover:bg-green-500/5 transition-colors group"
            >
              <div className="flex justify-between items-start mb-2">
                <h3 className="text-lg font-semibold text-green-400 group-hover:text-green-300">
                  &gt; Chapter {chapter.id}: {chapter.title}
                </h3>
                <span className="text-sm text-green-500/60">
                  {new Date(chapter.date).toLocaleDateString()}
                </span>
              </div>
              <p className="text-green-300/80 leading-relaxed">
                {chapter.summary}
              </p>
            </Link>
          ))}
        </div>
      </div>
    </section>
  )
} 