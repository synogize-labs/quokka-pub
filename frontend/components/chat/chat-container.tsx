"use client";

import { useEffect, useState } from "react";
import { createStyles } from "antd-style";
import { Spin } from "antd";
import { ChatSidebar } from "./chat-sidebar";
import { ChatMain } from "./chat-main";
import { useXAgent, useXChat } from "@ant-design/x";

const useStyles = createStyles(({ token, css }) => ({
  container: css`
    width: 100%;
    height: calc(100vh - 64px); // 减去 header 高度
    opacity: 0;
    animation: fadeIn 0.3s ease-in forwards;

    @keyframes fadeIn {
      from {
        opacity: 0;
      }
      to {
        opacity: 1;
      }
    }
  `,
  layout: css`
    height: 100%;
    width: 100%;
    display: flex;
    background: ${token.colorBgContainer};
    overflow: hidden;

    @media (max-width: 768px) {
      flex-direction: column;
    }
  `,
  loadingContainer: css`
    width: 100%;
    height: calc(100vh - 64px);
    display: flex;
    align-items: center;
    justify-content: center;
    background: ${token.colorBgContainer};
  `,
}));

export function ChatContainer() {
  const { styles } = useStyles();
  const [isLoading, setIsLoading] = useState(true);
  const [headerOpen, setHeaderOpen] = useState(false);
  const [content, setContent] = useState("");
  const [conversationsItems, setConversationsItems] = useState([
    { key: "0", label: "New Chat" },
  ]);
  const [activeKey, setActiveKey] = useState("0");
  const [attachedFiles, setAttachedFiles] = useState<any[]>([]);

  const [agent] = useXAgent({
    request: async ({ message }, { onSuccess }) => {
      onSuccess(
        `I received your message: "${message}". This is a demo response.`
      );
    },
  });

  const { onRequest, messages, setMessages } = useXChat({ agent });

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 1000);
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    if (activeKey !== undefined) {
      setMessages([]);
    }
  }, [activeKey]);

  if (isLoading) {
    return (
      <div className={styles.loadingContainer}>
        <Spin size="large" tip="Loading..." />
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.layout}>
        <ChatSidebar
          conversationsItems={conversationsItems}
          activeKey={activeKey}
          onAddConversation={() => {
            const newKey = `${conversationsItems.length}`;
            setConversationsItems([
              ...conversationsItems,
              { key: newKey, label: `New Chat ${conversationsItems.length}` },
            ]);
            setActiveKey(newKey);
          }}
          onConversationClick={setActiveKey}
        />
        <ChatMain
          messages={messages}
          content={content}
          headerOpen={headerOpen}
          attachedFiles={attachedFiles}
          agent={agent}
          onRequest={onRequest}
          setContent={setContent}
          setHeaderOpen={setHeaderOpen}
          setAttachedFiles={setAttachedFiles}
        />
      </div>
    </div>
  );
}
