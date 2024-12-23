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
                dangerouslySetInnerHTML={{ __html: paragraph }}
              />
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
        'SLAG is an AI-powered story engine that crafts long-form stories from a single user prompt.' +
        '<br/><br/>' +
        'By leveraging the power of LLMs, RAG, and parallelized recursive-prompting, SLAG is able to build complex worlds, develop rich characters, design and track plots, all autonomously.' +
        '<br/><br/>' +
        'What began as a project to generate a hard scifi graphic novel called "Starfall: Lost Age of Giants" has evolved into an abstract framework for generating any story in any genre.' +
        '<br/><br/>' +
        'SLAG is a tool built for artists, writers, creators, and communities alike.' +
        '<br/><br/>' +
        'To learn more, check out our Docs.'
    },
    {
      image: '/images/whatis$slag.png',
      alt: 'What is $SLAG token',
      backText: 
        '$SLAG will be a community token deployed on Solana. IT HAS NOT BEEN LAUNCHED YET.' +
        '<br/><br/>' +
        'The token will be used for interacting with the SLAG Story Engine and participating in SLAG DAO governance.' +
        '<br/><br/>' +
        'It has no inherent value and is meant for entertainment purposes only.' +
        '<br/><br/>' +
        'Purchasing cryptocurrencies is fraught with risk; you do so at your own peril and under your own free will.' +
        '<br/><br/>' +
        'Information regarding the token launch is detailed in our Docs (linked in header). Join our Telegram channel to stay up to date with the latest SLAG news.' +
        '<br/><br/>' +
        'None of this is financial advice. Do your own research and make your own decisions.',   
    },
    {
      image: '/images/officiallinks.png',
      alt: 'Official Links',
      backText: 
        '<a href="https://github.com/mango31/SLAG" target="_blank" rel="noopener noreferrer" class="text-green-600 hover:text-green-500 underline">GitHub</a>' +
        '<br/><br/>' +
        '<a href="https://x.com/slag_ai" target="_blank" rel="noopener noreferrer" class="text-green-600 hover:text-green-500 underline">X/Twitter</a>' +
        '<br/><br/>' +
        '<a href="https://t.me/slag_official" target="_blank" rel="noopener noreferrer" class="text-green-600 hover:text-green-500 underline">Telegram</a>' +
        '<br/><br/>' +
        '<a href="https://www.instagram.com/slag_ai" target="_blank" rel="noopener noreferrer" class="text-green-600 hover:text-green-500 underline">Instagram</a>' +
        '<br/><br/>' +
        '<a href="mailto:support@lostage.io" class="text-green-600 hover:text-green-500 underline">support@lostage.io</a>'
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