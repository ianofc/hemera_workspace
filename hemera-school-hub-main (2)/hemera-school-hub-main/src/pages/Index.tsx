import LandingNav from "@/components/landing/LandingNav";
import HeroSection from "@/components/landing/HeroSection";
import FeaturesSection from "@/components/landing/FeaturesSection";
import SegmentsSection from "@/components/landing/SegmentsSection";
import FooterSection from "@/components/landing/FooterSection";

const Index = () => (
  <div className="min-h-screen">
    <LandingNav />
    <HeroSection />
    <FeaturesSection />
    <SegmentsSection />
    <FooterSection />
  </div>
);

export default Index;
