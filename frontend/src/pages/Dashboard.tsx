import { Button } from "#components/ui/button";
import {
  MessageScrollerContent,
  MessageScrollerProvider,
  MessageScrollerViewport,
  MessageScrollerItem,
} from "#components/ui/message-scroller";
import { Textarea } from "#components/ui/textarea";
import { faPaperPlane } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { MessageScroller } from "#components/ui/message-scroller";
import axios from "axios";
import React, { useState } from "react";
import { Message, MessageContent } from "#components/ui/message";
import { Bubble, BubbleContent } from "#components/ui/bubble";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  text: string;
}

const Dashboard = () => {
  const [query, setQuery] = useState<string>();
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async (e?: React.SubmitEvent<HTMLFormElement>) => {
    if (e) e.preventDefault();

    const trimmed = query?.trim();
    if (!trimmed) return;

    const userMessage: ChatMessage = {
      id: `user-${Date.now()}`,
      role: "user",
      text: trimmed,
    };

    setQuery("");
    setMessages((prev) => [...prev, userMessage]);

    setLoading(true);
    try {
      const res = await axios.post(
        import.meta.env.VITE_API_BASE_URL + "/chat",
        {
          text: trimmed,
        },
      );

      const text: string = res.data?.text || "No response from AI";

      const assistantMessage: ChatMessage = {
        id: `bot-${Date.now()}`,
        role: "assistant",
        text: text,
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setLoading(false);
    } catch (e) {
      console.error(e);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();

      handleSubmit();
    }
  };

  return (
    <div className="flex justify-center flex-col items-center">
      <h2 className="text-red-500 text-2xl mt-2">Youtube Chatbot</h2>
      <div className="w-full max-w-4xl mt-12">
        <MessageScrollerProvider scrollPreviousItemPeek={64} scrollMargin={16}>
          <MessageScroller>
            <MessageScrollerViewport>
              <MessageScrollerContent>
                {messages.map((items) => {
                  const isUser = items.role === "user";

                  return (
                    <MessageScrollerItem
                      key={items.id}
                      messageId={items.id}
                      scrollAnchor={isUser}
                    >
                      <Message align={isUser ? "end" : "start"}>
                        <Bubble
                          variant={isUser ? "muted" : "ghost"}
                          align={isUser ? "end" : "start"}
                        >
                          <BubbleContent>
                            <p>{items.text}</p>
                          </BubbleContent>
                        </Bubble>
                      </Message>
                    </MessageScrollerItem>
                  );
                })}

                {loading && (
                  <Message align="start">
                    <MessageContent>
                      <Bubble variant="ghost" align="start">
                        <BubbleContent>
                          <p>Generating...</p>
                        </BubbleContent>
                      </Bubble>
                    </MessageContent>
                  </Message>
                )}
              </MessageScrollerContent>
            </MessageScrollerViewport>
          </MessageScroller>
        </MessageScrollerProvider>
      </div>

      <form
        className="absolute bottom-10 flex w-full justify-center items-center gap-4 "
        onSubmit={handleSubmit}
      >
        <Textarea
          className="max-w-4xl overflow-auto max-h-32 border-gray-950"
          placeholder="Ask anything"
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          required
          value={query}
        />
        <Button size={"lg"} className="bg-red-500">
          <FontAwesomeIcon icon={faPaperPlane} />
        </Button>
      </form>
    </div>
  );
};

export default Dashboard;
