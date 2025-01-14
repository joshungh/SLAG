import React from "react";
import { Box, Container, Typography, Paper } from "@mui/material";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export default function TermsPage() {
  return (
    <div className="min-h-screen text-green-400 font-['VT323']">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <Header />
        <Container maxWidth="lg" sx={{ py: 8 }}>
          <Paper elevation={3} sx={{ p: 4, bgcolor: "rgba(0,0,0,0.7)" }}>
            <Typography
              variant="h3"
              component="h1"
              gutterBottom
              sx={{ color: "#4ade80" }}
            >
              Terms of Use
            </Typography>

            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              Last Updated: {new Date().toLocaleDateString()}
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              1. Acceptance of Terms
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              By accessing and using SLAG Story Engine ("SLAG"), you accept and
              agree to be bound by these Terms of Use and our Privacy Policy.
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              2. Service Description
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              SLAG is an AI-powered story engine that creates long-form stories
              from user prompts using LLMs, RAG, and parallelized
              recursive-prompting technologies. The service is provided "as is"
              and may be modified or updated at any time.
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              3. User Content
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              You retain ownership of any content you submit to SLAG. By
              submitting content, you grant SLAG a worldwide, non-exclusive,
              royalty-free license to use, store, and process your content for
              the purpose of providing and improving our services.
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              4. AI-Generated Content
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              Stories generated through SLAG are created using artificial
              intelligence. While we strive for quality and originality, we
              cannot guarantee the uniqueness or appropriateness of AI-generated
              content. Users are responsible for reviewing and moderating
              generated content before use.
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              5. $SLAG Token
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              The $SLAG token is a community token with no inherent value and is
              meant for entertainment purposes only. Token usage is subject to
              separate terms and conditions. Cryptocurrency investments carry
              significant risks.
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              6. Intellectual Property
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              SLAG and its original content, features, and functionality are
              owned by Lost Age and are protected by international copyright,
              trademark, and other intellectual property laws.
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              7. Limitations of Liability
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              SLAG shall not be liable for any indirect, incidental, special,
              consequential, or punitive damages resulting from your use or
              inability to use the service.
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              8. Termination
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              We reserve the right to terminate or suspend access to our service
              immediately, without prior notice, for any reason including breach
              of these Terms.
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              9. Changes to Terms
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              We reserve the right to modify these terms at any time. We will
              notify users of any material changes via email or through the
              platform.
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              10. Contact Information
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              For questions about these Terms, please contact us at
              support@lostage.io
            </Typography>
          </Paper>
        </Container>
        <Footer />
      </div>
    </div>
  );
}
