// app/(marketing)/page.tsx
'use client';

import { Button, Space, Spin } from 'antd';
import { createStyles } from 'antd-style';
import { MessageSquare, RocketIcon, Wand2 } from 'lucide-react';
import Link from 'next/link';
import { useEffect, useState } from 'react';

const useStyles = createStyles(({ token, css }) => ({
  pageWrapper: css`
    opacity: 0;
    transition: opacity 0.3s ease-in;
    &.loaded {
      opacity: 1;
    }
  `,
  loadingContainer: css`
    width: 100vw;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: ${token.colorBgContainer};
  `,
  container: css`
    max-width: 1200px;
    margin: 0 auto;
    padding: 4rem 2rem;
  `,
  hero: css`
    text-align: center;
    margin-bottom: 4rem;
    h1 {
      margin-bottom: 1rem;
      font-size: 3rem;
      @media (max-width: 768px) {
        font-size: 2rem;
      }
    }
    p {
      font-size: 1.25rem;
      color: rgba(0, 0, 0, 0.65);
      margin-bottom: 2rem;
      @media (max-width: 768px) {
        font-size: 1rem;
      }
    }
  `,
  actionButton: css`
    height: 42px;
    padding: 0 24px;
    font-size: 16px;
    border-radius: 6px;
  `,
  secondaryButton: css`
    background: rgb(240, 242, 245);
    color: rgba(0, 0, 0, 0.88);
    &:hover {
      background: rgb(233, 236, 239) !important;
      color: rgba(0, 0, 0, 0.88) !important;
    }
  `,
  features: css`
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 2rem;
    margin-bottom: 4rem;
  `,
  feature: css`
    padding: 2rem;
    border-radius: ${token.borderRadius}px;
    background: ${token.colorBgContainer};
    box-shadow: ${token.boxShadowTertiary};
    text-align: center;
    h3 {
      margin: 1rem 0;
      font-size: 1.5rem;
    }
    p {
      color: ${token.colorTextSecondary};
    }
  `,
}));

export default function HomePage() {
  const { styles } = useStyles();
  const [loading, setLoading] = useState(true);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  if (!mounted) return null;

  if (loading) {
    return (
      <div className={styles.loadingContainer}>
        <Spin size="large" tip="Loading..." />
      </div>
    );
  }

  return (
    <div className={`${styles.pageWrapper} ${!loading ? 'loaded' : ''}`}>
      <div className={styles.container}>
        <section className={styles.hero}>
          <h1>AI Content Assistant</h1>
          <p>
            Generate, refine, and optimize your content with the power of AI
          </p>
          <Space size="large">
            {/* <Link href="/chat" passHref>
              <Button
                type="primary"
                className={styles.actionButton}
                icon={<MessageSquare size={16} />}
              >
                Start Chatting
              </Button>
            </Link> */}
            <Link href="/generate" passHref>
              <Button
                type="primary"
                className={`${styles.actionButton} ${styles.secondaryButton}`}
                icon={<Wand2 size={16} />}
              >
                Generate Content
              </Button>
            </Link>
          </Space>
        </section>

        <section className={styles.features}>
          <div className={styles.feature}>
            <RocketIcon size={32} />
            <h3>Smart Generation</h3>
            <p>Create engaging content tailored to your needs in seconds</p>
          </div>
          <div className={styles.feature}>
            <MessageSquare size={32} />
            <h3>Interactive Chat</h3>
            <p>Refine and improve your content through natural conversation</p>
          </div>
          <div className={styles.feature}>
            <Wand2 size={32} />
            <h3>Multiple Formats</h3>
            <p>Generate text, images, and more for various platforms</p>
          </div>
        </section>
      </div>
    </div>
  );
}
