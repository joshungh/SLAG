'use client'

import Image from "next/image"
import { useTrail, animated } from '@react-spring/web'

export default function Hero() {
  const items = [
    <span key="1" className="block text-[8rem] md:text-[12rem] lg:text-[16rem] mb-4 font-['Helvetica'] tracking-tighter text-[#fff1eb]">
      STARFALL
    </span>,
    <span key="2" className="block text-4xl md:text-6xl lg:text-8xl font-['Helvetica'] tracking-widest text-[#fff1eb]">
      LOST AGE OF GIANTS
    </span>
  ]

  const trail = useTrail(items.length, {
    from: { opacity: 0, y: 20 },
    to: { opacity: 1, y: 0 },
    config: { mass: 5, tension: 2000, friction: 200 },
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
            {trail.map((style, index) => (
              <animated.div key={index} style={style}>
                {items[index]}
              </animated.div>
            ))}
          </h1>
        </div>
      </div>
    </section>
  )
} 