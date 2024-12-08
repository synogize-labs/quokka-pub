// app/layout.tsx
"use client";

import "./globals.css";
import { Inter } from "next/font/google";
import { ConfigProvider, Layout, theme } from "antd";
import { AppHeader } from "@/components/layout/app-header";
import { createStyles } from "antd-style";
import { useEffect, useState } from "react";

const inter = Inter({ subsets: ["latin"] });

const useStyles = createStyles(({ token, css }) => ({
  layout: css`
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    visibility: hidden;
    &.loaded {
      visibility: visible;
    }
  `,
  main: css`
    flex: 1;
    width: 100%;
    margin: 0 auto;
    padding: 0;
    background: ${token.colorBgLayout};
  `,
  loadingContainer: css`
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: ${token.colorBgContainer};
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
  `,
}));

const themeConfig = {
  token: {
    borderRadius: 6,
    colorPrimary: "#1677ff",
  },
  components: {
    Button: {
      algorithm: true,
      colorPrimary: "#1677ff",
      colorPrimaryHover: "#4096ff",
      colorPrimaryActive: "#0958d9",
      primaryColor: "#fff",
      defaultBg: "#f0f2f5",
      defaultColor: "rgba(0, 0, 0, 0.88)",
      defaultBorderColor: "#d9d9d9",
      defaultHoverBg: "#e6e8eb",
      defaultHoverColor: "rgba(0, 0, 0, 0.88)",
      defaultHoverBorderColor: "#d9d9d9",
      controlTmpOutline: "none",
      colorTextLightSolid: "#ffffff",
      primaryShadow: "none",
      primaryShadowHover: "none",
    },
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { styles } = useStyles();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Add a small delay to ensure styles are loaded
    const timer = setTimeout(() => {
      setLoading(false);
    }, 300);

    return () => clearTimeout(timer);
  }, []);

  return (
    <html lang="en" className={inter.className}>
      <head>
        <style>{`
          /* Prevent FOUC */
          html {
            visibility: visible;
          }
        `}</style>
      </head>
      <body>
        <ConfigProvider
          theme={{
            ...themeConfig,
            algorithm: theme.defaultAlgorithm,
          }}
        >
          <Layout className={`${styles.layout} ${!loading ? "loaded" : ""}`}>
            <AppHeader />
            <Layout.Content className={styles.main}>{children}</Layout.Content>
          </Layout>
        </ConfigProvider>
      </body>
    </html>
  );
}
