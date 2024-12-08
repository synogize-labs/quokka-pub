// app/loading.tsx
"use client";

import { Spin } from "antd";
import { createStyles } from "antd-style";

const useStyles = createStyles(({ token, css }) => ({
  container: css`
    width: 100vw;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: ${token.colorBgContainer};
  `,
}));

export default function Loading() {
  const { styles } = useStyles();
  return (
    <div className={styles.container}>
      <Spin size="large" tip="Loading..." />
    </div>
  );
}
