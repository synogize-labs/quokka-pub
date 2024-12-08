'use client';

import { Layout, Menu, Spin } from 'antd';
import { createStyles } from 'antd-style';
import { Home, MessageSquare, Wand2 } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';

const { Header } = Layout;

const useStyles = createStyles(({ token, css }) => ({
  headerWrapper: css`
    opacity: 0;
    transition: opacity 0.3s ease-in;
    &.loaded {
      opacity: 1;
    }
  `,
  loadingContainer: css`
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: ${token.colorBgContainer};
    border-bottom: 1px solid ${token.colorBorderSecondary};
  `,
  header: css`
    background: ${token.colorBgContainer};
    border-bottom: 1px solid ${token.colorBorderSecondary};
    display: flex;
    align-items: center;
  `,
  container: css`
    max-width: 1200px;
    width: 100%;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 ${token.padding}px;
  `,
  logo: css`
    font-size: 1.5rem;
    font-weight: bold;
    color: ${token.colorText};
    text-decoration: none;
    white-space: nowrap;
  `,
  menu: css`
    flex: 1;
    justify-content: flex-end;
    border: none;
    background: transparent;
  `,
}));

export function AppHeader() {
  const { styles } = useStyles();
  const pathname = usePathname();
  const [loading, setLoading] = useState(true);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const timer = setTimeout(() => {
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  const items = [
    {
      key: '/',
      icon: <Home size={16} />,
      label: <Link href="/">Home</Link>,
    },
    // {
    //   key: "/chat",
    //   icon: <MessageSquare size={16} />,
    //   label: <Link href="/chat">Chat</Link>,
    // },
    {
      key: '/generate',
      icon: <Wand2 size={16} />,
      label: <Link href="/generate">Generate</Link>,
    },
  ];

  if (!mounted) return null;

  if (loading) {
    return (
      <div className={styles.loadingContainer}>
        <Spin size="small" />
      </div>
    );
  }

  return (
    <Header
      className={`${styles.headerWrapper} ${!loading ? 'loaded' : ''} ${
        styles.header
      }`}
    >
      <div className={styles.container}>
        <Link href="/" className={styles.logo}>
          AI Assistant
        </Link>
        <Menu
          mode="horizontal"
          selectedKeys={[pathname]}
          items={items}
          className={styles.menu}
        />
      </div>
    </Header>
  );
}
