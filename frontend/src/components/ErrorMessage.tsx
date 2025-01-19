import { motion } from "framer-motion";

interface ErrorMessageProps {
  message: string | null;
}

export default function ErrorMessage({ message }: ErrorMessageProps) {
  if (!message) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: -10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-red-500/10 border border-red-500 text-red-400 text-sm p-3 rounded-lg"
    >
      {message}
    </motion.div>
  );
}
