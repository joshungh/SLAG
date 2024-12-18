import Image from 'next/image'
import Link from 'next/link'

interface ChapterPageProps {
  params: {
    slug: string
  }
}

export default function ChapterPage({ params }: ChapterPageProps) {
  return (
    <div className="min-h-screen bg-[#0a0f14] py-8">
      <div className="max-w-3xl mx-auto px-4">
        {/* Navigation */}
        <Link 
          href="/"
          className="inline-flex items-center text-green-400 hover:text-green-300 mb-8"
        >
          &lt; Back to Archives
        </Link>

        {/* Chapter Content */}
        <article className="prose prose-invert prose-green max-w-none">
          <h1 className="text-4xl font-bold text-green-400 mb-8">
            Chapter 1: The Awakening
          </h1>
          
          <div className="space-y-8">
            <p className="text-lg leading-relaxed">
              The ancient machinery hummed beneath layers of dust and forgotten memories...
            </p>

            <figure className="relative aspect-video my-12">
              <Image
                src="/images/mango.coca_scifi_fantasy_graphic_novel_giants_a_war_rich_detail_e1c177c6-d3b4-4777-b7c8-912c8a6cb6fd.png"
                alt="Chapter illustration"
                fill
                className="object-cover rounded-lg"
              />
            </figure>

            {/* More story content */}
          </div>
        </article>
      </div>
    </div>
  )
} 