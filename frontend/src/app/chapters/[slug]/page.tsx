import Image from 'next/image'
import Link from 'next/link'
import { Metadata } from 'next'
import { notFound } from 'next/navigation'

const chapters = {
  'chapter-1-the-awakening': {
    id: 1,
    title: "The Awakening",
    content: "The ancient machinery hummed beneath layers of dust and forgotten memories...",
    image: "/images/mango.coca_scifi_fantasy_graphic_novel_giants_a_war_rich_detail_e1c177c6-d3b4-4777-b7c8-912c8a6cb6fd.png"
  },
  'chapter-2-echoes-of-giants': {
    id: 2,
    title: "Echoes of the Giants",
    content: "As the truth about the ancient civilization emerges, our heroes face an impossible choice...",
    image: "/images/mango.coca_scifi_fantasy_graphic_novel_giants_a_war_rich_detail_579b4bdb-f763-420e-84cf-602c7509c1f8.png"
  }
} as const

export default function ChapterPage({
  params,
}: {
  params: { slug: string }
}) {
  const chapter = chapters[params.slug as keyof typeof chapters]
  if (!chapter) notFound()

  return (
    <div className="min-h-screen bg-[#0a0f14] py-8">
      <div className="max-w-3xl mx-auto px-4">
        <Link 
          href="/"
          className="inline-flex items-center text-green-400 hover:text-green-300 mb-8"
        >
          &lt; Back to Archives
        </Link>

        <article className="prose prose-invert prose-green max-w-none">
          <h1 className="text-4xl font-bold text-green-400 mb-8">
            Chapter {chapter.id}: {chapter.title}
          </h1>
          
          <div className="space-y-8">
            <p className="text-lg leading-relaxed">
              {chapter.content}
            </p>

            <figure className="relative aspect-video my-12">
              <Image
                src={chapter.image}
                alt={`Chapter ${chapter.id} illustration`}
                fill
                className="object-cover rounded-lg"
              />
            </figure>
          </div>
        </article>
      </div>
    </div>
  )
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const chapter = chapters[params.slug]
  if (!chapter) return { title: 'Chapter Not Found' }
  
  return {
    title: `Chapter ${chapter.id}: ${chapter.title} | Starfall: Lost Age of Giants`,
    description: chapter.content.substring(0, 155) + '...',
    openGraph: {
      title: `Chapter ${chapter.id}: ${chapter.title} | Starfall: Lost Age of Giants`,
      description: chapter.content.substring(0, 155) + '...',
      images: [
        {
          url: chapter.image,
          width: 1200,
          height: 630,
          alt: `Chapter ${chapter.id}: ${chapter.title}`,
        },
      ],
    },
    twitter: {
      card: 'summary_large_image',
      title: `Chapter ${chapter.id}: ${chapter.title}`,
      description: chapter.content.substring(0, 155) + '...',
      images: [chapter.image],
    },
  }
}