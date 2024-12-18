'use client'

import { useState, useEffect } from 'react'

export default function StoryFeed() {
  const [chapters, setChapters] = useState([
    {
      id: 1,
      title: "Chapter 1: The Awakening",
      scenes: [
        {
          id: 1,
          content: "In the shadow of forgotten titans, a lone traveler embarks on a perilous journey...",
        }
      ]
    }
  ])

  useEffect(() => {
    // Simulated data fetching
    const fetchData = async () => {
      const newChapter = {
        id: chapters.length + 1,
        title: `Chapter ${chapters.length + 1}: The Unfolding Mystery`,
        scenes: [
          {
            id: chapters[chapters.length - 1].scenes.length + 1,
            content: "As the traveler ventured deeper into the unknown, ancient secrets began to reveal themselves...",
          }
        ]
      }
      setChapters(prevChapters => [...prevChapters, newChapter])
    }

    const interval = setInterval(fetchData, 30000)
    return () => clearInterval(interval)
  }, [chapters])

  return (
    <section id="story" className="space-y-8">
      <h2 className="text-xl font-bold text-green-500">&gt; Story_Feed</h2>
      <div className="border border-green-500 rounded-lg overflow-hidden">
        <div className="bg-gray-800 text-green-400 px-4 py-2 font-bold">
          &gt; Story Generation Logs
        </div>
        <div className="bg-black p-4 h-96 overflow-y-auto">
          {chapters.map((chapter) => (
            <div key={chapter.id} className="mb-4">
              <h3 className="text-lg font-semibold mb-2 text-green-400">&gt; {chapter.title}</h3>
              {chapter.scenes.map((scene) => (
                <div key={scene.id} className="mb-2 last:mb-0">
                  <p className="text-green-300 leading-relaxed">{scene.content}</p>
                </div>
              ))}
            </div>
          ))}
        </div>
      </div>
    </section>
  )
} 