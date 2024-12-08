import { Message } from "@/lib/types";
import { cn } from "@/lib/utils";
import { Bot, User } from "lucide-react";

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const isAssistant = message.role === "assistant";

  return (
    <div
      className={cn(
        "flex items-start gap-4 rounded-lg p-4",
        isAssistant ? "bg-muted/50" : "bg-background"
      )}
    >
      <div className="flex h-8 w-8 shrink-0 select-none items-center justify-center rounded-md border bg-background">
        {isAssistant ? <Bot size={18} /> : <User size={18} />}
      </div>
      <div className="flex-1 space-y-2">
        <p className="text-sm font-medium">
          {isAssistant ? "Assistant" : "You"}
        </p>
        <div className="text-sm text-muted-foreground">
          {message.content}
        </div>
      </div>
    </div>
  );
}