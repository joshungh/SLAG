'use client'

import Image from 'next/image'
import { useState } from 'react'
import { useSpring, a } from '@react-spring/web'

interface CardProps {
  image: string
  alt: string
  backText: string
}

function FlipCard({ image, alt, backText }: CardProps) {
  const [flipped, setFlipped] = useState(false)

  const { transform, opacity } = useSpring({
    opacity: flipped ? 1 : 0,
    transform: `perspective(600px) rotateY(${flipped ? 180 : 0}deg)`,
    config: { mass: 5, tension: 500, friction: 80 }
  })

  const paragraphs = backText.split('<br/><br/>')

  return (
    <div
      className="relative w-full aspect-square cursor-pointer"
      onClick={() => setFlipped(state => !state)}
    >
      <a.div
        className="absolute w-full h-full rounded-xl"
        style={{
          opacity: opacity.to(o => 1 - o),
          transform,
          rotateY: '0deg'
        }}
      >
        {/* Front of card */}
        <div className="w-full h-full rounded-xl border border-green-500/20 overflow-hidden">
          <Image
            src={`${image}?v=2`}
            alt={alt}
            fill
            className="object-cover rounded-xl"
            priority
          />
        </div>
      </a.div>

      <a.div
        className="absolute w-full h-full rounded-xl bg-white"
        style={{
          opacity,
          transform,
          rotateY: '180deg',
          backfaceVisibility: 'hidden'
        }}
      >
        {/* Back of card */}
        <div className="absolute inset-0 p-4 overflow-y-auto">
          <div className="space-y-3 text-left">
            {paragraphs.map((paragraph, index) => (
              <p 
                key={index} 
                className="font-['IBM_Plex_Mono'] text-black text-sm leading-relaxed"
              >
                {paragraph}
              </p>
            ))}
          </div>
        </div>
      </a.div>
    </div>
  )
}

export default function InfoSection() {
  const cards = [
    {
      image: '/images/whatisslag.png',
      alt: 'What is SLAG',
      backText: 
        'Starfall: Lost Age of Giants (SLAG for short) is a human-guided but autonomously-generated epic graphic novel.' +
        '<br/><br/>' +
        'A love child born from two obsessions:' +
        '<br/><br/>' +
        'A deep rooted admiration towards the work of John Scalzi, Joe Haldeman, Isaac Asimov, and Frank Herbert.' +
        '<br/><br/>' +
        'A fascination with LLMs and the world we find ourselves in.' +
        '<br/><br/>' +
        'SLAG is first and foremost an artistic journey. As such, expect bumps, bruises, laughter, longing, and perhaps the occasional hallucination.'
    },
    {
      image: '/images/whatis$slag.png',
      alt: 'What is $SLAG token',
      backText: 
        '$SLAG is a community token deployed on Solana.' +
        '<br/><br/>' +
        'It has no inherent value and is meant for entertainment purposes only.' +
        '<br/><br/>' +
        'Purchasing cryptocurrencies is fraught with risk; you do so at your own risk.' +
        '<br/><br/>' +
        'The token will be stealth launched on pump.fun in December 2024.'
    },
    {
      image: '/images/officiallinks.png',
      alt: 'Official Links',
      backText: 
        'GitHub Repository:' +
        '<br/><br/>' +
        'https://github.com/mango31/SLAG'
    }
  ]

  return (
    <section id="info" className="grid grid-cols-1 md:grid-cols-3 gap-8">
      {cards.map((card, index) => (
        <FlipCard key={index} {...card} />
      ))}
    </section>
  )
} 