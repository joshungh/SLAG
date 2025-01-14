import Header from "@/components/Header";
import Hero from "@/components/Hero";
import Footer from "@/components/Footer";
import InfoSection from "@/components/InfoSection";
import SampleOutput from "@/components/SampleOutput";

export default function Home() {
  return (
    <div className="min-h-screen text-green-400 font-['VT323']">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <Header />
        <Hero />
        <main className="mt-12 space-y-16">
          <InfoSection />
          <SampleOutput />
        </main>
        <Footer />
      </div>
    </div>
  );
}
