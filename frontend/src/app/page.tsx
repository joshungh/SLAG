import Header from '@/components/Header'
import Hero from '@/components/Hero'
import StoryFeed from '@/components/StoryFeed'
import Footer from '@/components/Footer'
import CloudwatchLogsBox from '@/components/CloudwatchLogsBox'
import InfoSection from '@/components/InfoSection'

export default function Home() {
  return (
    <div className="min-h-screen bg-[#0a0f14] text-green-400 font-['VT323']">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <Header />
        <Hero />
        <main className="mt-12 space-y-16">
          <InfoSection />
          <StoryFeed />
          <section className="mt-8">
            <CloudwatchLogsBox />
          </section>
        </main>
        <Footer />
      </div>
    </div>
  )
}
