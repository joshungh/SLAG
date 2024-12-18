import Image from "next/image"

export default function Hero() {
  return (
    <section className="relative overflow-hidden border border-green-500 rounded-lg mb-8">
      <div className="relative z-10 grid lg:grid-cols-2 gap-8 items-center p-8">
        <div className="space-y-6">
          <div className="space-y-2">
            <h2 className="text-4xl font-bold tracking-tighter">
              &gt; DISCOVER_THE_LOST_AGE
              <span className="animate-pulse">▋</span>
            </h2>
            <p className="text-xl text-green-400/80">
              An AI-generated graphic novel exploring the remnants of a forgotten civilization. 
              Watch as the story unfolds in real-time through machine learning and autonomous storytelling.
            </p>
          </div>
          <div className="flex gap-4">
            <button 
              className="bg-green-500 hover:bg-green-600 text-black font-mono px-4 py-2 rounded"
            >
              &gt; BEGIN_EXPLORATION
            </button>
            <button 
              className="border border-green-500 text-green-400 hover:bg-green-500/10 font-mono px-4 py-2 rounded"
            >
              &gt; VIEW_ARCHIVES
            </button>
          </div>
        </div>
        <div className="relative aspect-[4/3] lg:aspect-[3/4] overflow-hidden rounded border border-green-500/50">
          <Image
            src="/images/mango.coca_scifi_fantasy_graphic_novel_a_war_rich_detail_in_the_04edfcc5-fd56-43bd-a435-2dc7e4a8c791.png"
            alt="A lone figure perched on ancient machinery against a red sky"
            fill
            className="object-cover"
            priority
          />
          <div className="absolute inset-0 bg-gradient-to-r from-[#0a0f14] via-transparent to-transparent lg:via-[#0a0f14]/50 lg:to-[#0a0f14]" />
        </div>
      </div>
      <div className="absolute inset-0 pointer-events-none border border-green-500 rounded-lg opacity-20">
        <div className="h-full w-full bg-[linear-gradient(to_right,transparent_0%,transparent_49%,#4ade80_49%,#4ade80_51%,transparent_51%,transparent_100%)] bg-[length:4rem_100%] animate-scan" />
      </div>
    </section>
  )
} 