"use client";

import { Button } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import { Conversations } from "@ant-design/x";
import { createStyles } from "antd-style";

const useStyles = createStyles(({ token, css }) => ({
  menu: css`
    background: ${token.colorBgLayout}80;
    width: 280px;
    height: 100%;
    display: flex;
    flex-direction: column;
    border-right: 1px solid ${token.colorBorder};

    @media (max-width: 768px) {
      width: 100%;
      height: auto;
      border-right: none;
      border-bottom: 1px solid ${token.colorBorder};
    }
  `,
  logo: css`
    display: flex;
    height: 72px;
    align-items: center;
    padding: 0 24px;
    border-bottom: 1px solid ${token.colorBorder};

    span {
      font-size: ${token.fontSizeLG}px;
      font-weight: 600;
      color: ${token.colorText};
    }

    @media (max-width: 768px) {
      height: 56px;
    }
  `,
  addBtn: css`
    background: ${token.colorPrimaryBg};
    border: 1px solid ${token.colorPrimaryBorder};
    width: calc(100% - 24px);
    margin: 12px;

    &:hover {
      background: ${token.colorPrimaryBgHover};
    }
  `,
  conversations: css`
    flex: 1;
    overflow-y: auto;
    padding: 0 12px;

    &::-webkit-scrollbar {
      width: 6px;
    }

    &::-webkit-scrollbar-thumb {
      background: ${token.colorBorder};
      border-radius: 3px;
    }
  `,
}));

interface ChatSidebarProps {
  conversationsItems: Array<{ key: string; label: string }>;
  activeKey: string;
  onAddConversation: () => void;
  onConversationClick: (key: string) => void;
}

export function ChatSidebar({
  conversationsItems,
  activeKey,
  onAddConversation,
  onConversationClick,
}: ChatSidebarProps) {
  const { styles } = useStyles();

  return (
    <div className={styles.menu}>
      <Button
        onClick={onAddConversation}
        type="link"
        className={styles.addBtn}
        icon={<PlusOutlined />}
      >
        New Chat
      </Button>
      <div className={styles.conversations}>
        <Conversations
          items={conversationsItems}
          activeKey={activeKey}
          onActiveChange={onConversationClick}
        />
      </div>
    </div>
  );
}
