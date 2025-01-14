import React from "react";
import { Box, Container, Typography, Paper } from "@mui/material";
import Header from "@/components/Header";
import Footer from "@/components/Footer";

export default function PrivacyPage() {
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
              Privacy Policy
            </Typography>

            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              Last Updated: {new Date().toLocaleDateString()}
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              1. Introduction
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              SLAG Story Engine ("SLAG", "we", "us", or "our") is committed to
              protecting your privacy. This Privacy Policy explains how we
              collect, use, disclose, and safeguard your information when you
              use our service.
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              2. Information We Collect
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              We collect information that you provide directly to us, including:
              • Account information (email, username, password) • Story prompts
              and generated content • Payment information (processed securely
              through third-party providers) • Communication preferences • Usage
              data and interaction with our platform
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              3. How We Use Your Information
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              We use the collected information to: • Provide and maintain our
              service • Improve our AI story generation capabilities • Process
              your transactions • Send you updates and notifications • Respond
              to your inquiries • Analyze usage patterns and optimize user
              experience • Comply with legal obligations
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              4. Data Storage and Security
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              We implement appropriate technical and organizational measures to
              protect your personal information. Your data is stored securely on
              AWS servers with industry-standard encryption and security
              protocols.
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              5. AI Training Data
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              User-generated prompts and stories may be used to improve our AI
              models. All data used for AI training is anonymized and stripped
              of personal identifiers. You can opt out of having your content
              used for AI training through your account settings.
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              6. Information Sharing
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              We do not sell your personal information. We may share your
              information with: • Service providers who assist in our operations
              • Legal authorities when required by law • Business partners with
              your consent
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              7. Your Rights
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              You have the right to: • Access your personal information •
              Correct inaccurate data • Request deletion of your data • Opt out
              of marketing communications • Export your data
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              8. Cookies and Tracking
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              We use cookies and similar tracking technologies to improve user
              experience and analyze platform usage. You can control cookie
              preferences through your browser settings.
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              9. Children's Privacy
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              Our service is not intended for users under 13 years of age. We do
              not knowingly collect information from children under 13.
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              10. Changes to Privacy Policy
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              We may update this Privacy Policy periodically. We will notify you
              of any material changes via email or through the platform.
            </Typography>

            <Typography
              variant="h5"
              gutterBottom
              sx={{ mt: 4, color: "#4ade80" }}
            >
              11. Contact Us
            </Typography>
            <Typography variant="body1" paragraph sx={{ color: "#4ade80" }}>
              If you have questions about this Privacy Policy, please contact us
              at privacy@lostage.io
            </Typography>
          </Paper>
        </Container>
        <Footer />
      </div>
    </div>
  );
}
