'use client'

import Image from "next/image"
import { useTrail, animated } from '@react-spring/web'
import { useEffect, useState } from 'react'

export default function Hero() {
  const [isClient, setIsClient] = useState(false)

  useEffect(() => {
    setIsClient(true)
  }, [])

  const items = [
    <span key="1" className="block text-[2rem] sm:text-[3rem] md:text-[5rem] lg:text-[7rem] mb-4 font-['Helvetica'] tracking-tighter text-[#fff1eb]">
      SLAG STORY ENGINE
    </span>,
    <span key="2" className="block text-base sm:text-lg md:text-2xl lg:text-4xl font-['Helvetica'] tracking-widest text-[#fff1eb]">
      A SINGLE PROMPT TO RULE THEM ALL
    </span>
  ]

  const trail = useTrail(items.length, {
    from: { opacity: 0, y: 50 },
    to: { opacity: 1, y: 0 },
    config: { 
      tension: 80,
      friction: 20,
      mass: 1.5
    }
  })

  return (
    <section className="relative h-screen">
      <div className="absolute inset-0">
        <Image
          src="/images/mango.coca_scifi_fantasy_graphic_novel_giants_a_war_rich_detail_e1c177c6-d3b4-4777-b7c8-912c8a6cb6fd.png"
          alt="Dystopian sci-fi landscape"
          fill
          className="object-cover"
          priority
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent" />
      </div>

      <div className="relative z-10 flex items-center justify-center h-full">
        <div className="text-center px-4">
          <h1 className="font-black leading-none tracking-tight">
            {!isClient ? (
              items.map((item, index) => (
                <div key={index} className="opacity-100">
                  {item}
                </div>
              ))
            ) : (
              trail.map((props, index) => (
                <animated.div 
                  key={index} 
                  style={{
                    opacity: props.opacity,
                    transform: props.y.to(y => `translateY(${y}px)`)
                  }}
                >
                  {items[index]}
                </animated.div>
              ))
            )}
          </h1>
        </div>
      </div>
    </section>
  )
} 