'use client';

import { createStyles } from 'antd-style';

interface TrendingTopicsProps {
  topics: string[];
  onTopicClick: (topic: string) => void;
}

const useStyles = createStyles(({ token, css }) => ({
  container: css`
    margin: 1rem 0;
  `,
  topics: css`
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  `,
  topic: css`
    background: ${token.colorBgContainer};
    border: 1px solid ${token.colorBorder};
    padding: 0.25rem 0.75rem;
    border-radius: ${token.borderRadius}px;
    font-size: 0.875rem;
    color: ${token.colorTextSecondary};
    cursor: pointer;
    transition: all 0.2s;

    &:hover {
      background: ${token.colorBgTextHover};
      color: ${token.colorPrimary};
      border-color: ${token.colorPrimary};
    }

    &::before {
      content: '#';
      margin-right: 0.25rem;
      color: ${token.colorPrimary};
    }
  `,
}));

export function TrendingTopics({ topics, onTopicClick }: TrendingTopicsProps) {
  const { styles } = useStyles();

  return (
    <div className={styles.container}>
      <div className="text-sm font-medium mb-2">Trending Topics</div>
      <div className={styles.topics}>
        {topics.map((topic) => (
          <button
            key={topic}
            className={styles.topic}
            onClick={() => onTopicClick(topic)}
          >
            {topic}
          </button>
        ))}
      </div>
    </div>
  );
}
