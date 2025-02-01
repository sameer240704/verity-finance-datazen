import { motion } from "framer-motion";
import { User, BotMessageSquare, Volume2, VolumeX } from "lucide-react";

interface Message {
  type: "user" | "bot";
  content: string | string[];
  timestamp: Date;
  isThinking?: boolean;
}

interface MessageFormatterProps {
  messages: Message[];
  speak: (content: string, index: number) => void;
  isSpeaking: number | null;
  messagesEndRef: React.RefObject<HTMLDivElement>;
}

const MessageFormatter: React.FC<MessageFormatterProps> = ({
  messages,
  speak,
  isSpeaking,
  messagesEndRef,
}) => {
  // Function to format text with links and bold styling
  const formatMessage = (content: string | string[]): React.ReactNode => {
    if (typeof content !== "string") return content;

    return content.split(/(\*\*.*?\*\*|\[.*?\]\(.*?\))/g).map((part, index) => {
      if (part.startsWith("**") && part.endsWith("**")) {
        return (
          <strong key={index} className="font-bold">
            {part.slice(2, -2)}
          </strong>
        );
      }
      if (part.startsWith("[") && part.includes("](")) {
        const match = part.match(/\[(.*?)\]\((.*?)\)/);
        if (match) {
          return (
            <a
              key={index}
              href={match[2]}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline"
            >
              {match[1]}
            </a>
          );
        }
      }
      return <span key={index}>{part}</span>;
    });
  };

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-4">
      {messages.map((message, index) => (
        <motion.div
          key={index}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className={`flex ${
            message.type === "user" ? "justify-end" : "justify-start"
          }`}
        >
          <div
            className={`flex items-start space-x-2 max-w-[80%] ${
              message.type === "user" ? "flex-row-reverse space-x-reverse" : ""
            }`}
          >
            <div
              className={`p-2 rounded-lg ${
                message.type === "user"
                  ? "bg-primary-600"
                  : "bg-gray-100 dark:bg-gray-700"
              }`}
            >
              {message.type === "user" ? (
                <User className="h-5 w-5 text-white" />
              ) : (
                <BotMessageSquare className="h-5 w-5 text-primary-600 dark:text-primary-400" />
              )}
            </div>
            <div
              className={`relative p-4 rounded-2xl ${
                message.type === "user"
                  ? "bg-primary-600 text-white"
                  : "bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white"
              }`}
            >
              <div className="text-sm whitespace-pre-line">
                {Array.isArray(message.content)
                  ? message.content.map((line, i) => (
                      <motion.div
                        key={i}
                        initial={
                          message.isThinking ? { opacity: 0 } : { opacity: 1 }
                        }
                        animate={{ opacity: 1 }}
                        transition={{ duration: 0.5 }}
                        className={`${
                          line.startsWith("🤔")
                            ? "font-semibold text-primary-600 dark:text-primary-400"
                            : line.startsWith("───")
                            ? "text-gray-400 dark:text-gray-500"
                            : message.isThinking &&
                              i === message.content.length - 1
                            ? "text-gray-600 dark:text-gray-400"
                            : ""
                        }`}
                      >
                        {formatMessage(line)}
                      </motion.div>
                    ))
                  : formatMessage(message.content)}
              </div>
              <div className="flex items-center justify-between mt-1">
                <p className="text-xs opacity-70">
                  {message.timestamp.toLocaleTimeString([], {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </p>
                {message.type === "bot" && !message.isThinking && (
                  <button
                    onClick={() =>
                      speak(
                        Array.isArray(message.content)
                          ? message.content.join("\n")
                          : message.content,
                        index
                      )
                    }
                    className={`ml-2 p-1 rounded-full transition-colors ${
                      isSpeaking === index
                        ? "bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400"
                        : "hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-500 dark:text-gray-400"
                    }`}
                  >
                    {isSpeaking === index ? (
                      <VolumeX className="h-4 w-4" />
                    ) : (
                      <Volume2 className="h-4 w-4" />
                    )}
                  </button>
                )}
              </div>
            </div>
          </div>
        </motion.div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageFormatter;
