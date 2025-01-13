import ImageGallery from "@/components/ImageGallery";
import { galleryImages } from "@/data/images";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export default function GalleryPage() {
  return (
    <div className="min-h-screen text-green-400 font-['VT323']">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <Header />
        <main className="mt-12">
          <ImageGallery images={galleryImages} />
        </main>
        <Footer />
      </div>
    </div>
  );
}
