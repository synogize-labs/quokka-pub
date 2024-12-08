"use client";

import { createStyles } from 'antd-style';
import {
  Attachments,
  Bubble,
  Prompts,
  Sender,
  Welcome,
} from '@ant-design/x';
import {
  FireOutlined,
  ReadOutlined,
  ShareAltOutlined,
  EllipsisOutlined,
  CloudUploadOutlined,
  PaperClipOutlined,
} from '@ant-design/icons';
import { Badge, Button, Space } from 'antd';
import type { GetProp } from 'antd';

const useStyles = createStyles(({ token, css }) => ({
  chat: css`
    height: 100%;
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: ${token.paddingLG}px;
    gap: 16px;
    overflow: hidden;
    
    @media (max-width: 768px) {
      padding: ${token.paddingMD}px;
    }
  `,
  messages: css`
    flex: 1;
    overflow-y: auto;
    padding-right: ${token.paddingXS}px;
    
    &::-webkit-scrollbar {
      width: 6px;
    }
    
    &::-webkit-scrollbar-thumb {
      background: ${token.colorBorder};
      border-radius: 3px;
    }
  `,
  sender: css`
    box-shadow: ${token.boxShadowSecondary};
  `
}));

const senderPromptsItems = [
  {
    key: '1',
    description: 'Hot Topics',
    icon: <FireOutlined style={{ color: '#FF4D4F' }} />,
  },
  {
    key: '2',
    description: 'Design Guide',
    icon: <ReadOutlined style={{ color: '#1890FF' }} />,
  },
];

const roles: GetProp<typeof Bubble.List, 'roles'> = {
  ai: {
    placement: 'start',
    typing: { step: 5, interval: 20 },
    styles: {
      content: {
        borderRadius: 16,
      },
    },
  },
  local: {
    placement: 'end',
    variant: 'shadow',
  },
};

interface ChatMainProps {
  messages: any[];
  content: string;
  headerOpen: boolean;
  attachedFiles: any[];
  agent: any;
  onRequest: (message: string) => void;
  setContent: (content: string) => void;
  setHeaderOpen: (open: boolean) => void;
  setAttachedFiles: (files: any[]) => void;
}

export function ChatMain({
  messages,
  content,
  headerOpen,
  attachedFiles,
  agent,
  onRequest,
  setContent,
  setHeaderOpen,
  setAttachedFiles,
}: ChatMainProps) {
  const { styles } = useStyles();

  const welcomeNode = (
    <Space direction="vertical" size={16} style={{ paddingTop: 32 }}>
      <Welcome
        variant="borderless"
        icon="https://mdn.alipayobjects.com/huamei_iwk9zp/afts/img/A*s5sNRo5LjfQAAAAAAAAAAAAADgCCAQ/fmt.webp"
        title="Hello, I'm your AI Assistant"
        description="I'm here to help answer your questions and assist with tasks."
        extra={
          <Space>
            <Button icon={<ShareAltOutlined />} />
            <Button icon={<EllipsisOutlined />} />
          </Space>
        }
      />
    </Space>
  );

  const items: GetProp<typeof Bubble.List, 'items'> = messages.map(({ id, message, status }) => ({
    key: id,
    loading: status === 'loading',
    role: status === 'local' ? 'local' : 'ai',
    content: message,
  }));

  const attachmentsNode = (
    <Badge dot={attachedFiles.length > 0 && !headerOpen}>
      <Button 
        type="text" 
        icon={<PaperClipOutlined />} 
        onClick={() => setHeaderOpen(!headerOpen)} 
      />
    </Badge>
  );

  const senderHeader = (
    <Sender.Header
      title="Attachments"
      open={headerOpen}
      onOpenChange={setHeaderOpen}
      styles={{
        content: {
          padding: 0,
        },
      }}
    >
      <Attachments
        beforeUpload={() => false}
        items={attachedFiles}
        onChange={(info) => setAttachedFiles(info.fileList)}
        placeholder={(type) =>
          type === 'drop'
            ? { title: 'Drop file here' }
            : {
                icon: <CloudUploadOutlined />,
                title: 'Upload files',
                description: 'Click or drag files to this area to upload',
              }
        }
      />
    </Sender.Header>
  );

  return (
    <div className={styles.chat}>
      <Bubble.List
        items={items.length > 0 ? items : [{ content: welcomeNode, variant: 'borderless' }]}
        roles={roles}
        className={styles.messages}
      />
      <Prompts 
        items={senderPromptsItems} 
        onItemClick={(info) => onRequest(info.data.description as string)} 
      />
      <Sender
        value={content}
        header={senderHeader}
        onSubmit={(nextContent) => {
          if (!nextContent) return;
          onRequest(nextContent);
          setContent('');
        }}
        onChange={setContent}
        prefix={attachmentsNode}
        loading={agent.isRequesting()}
        className={styles.sender}
      />
    </div>
  );
}