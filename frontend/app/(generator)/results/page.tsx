"use client";

import { useEffect, useState } from "react";
import { Card, Button, Input, Space, Typography } from "antd";
import { createStyles } from "antd-style";
import { Download, RefreshCw, ThumbsUp, ThumbsDown } from "lucide-react";

const { TextArea } = Input;
const { Title, Text } = Typography;

interface GeneratedResult {
  content: string;
  metadata: {
    tone: string;
    format: string;
    platform: string;
    timestamp: string;
  };
}

const useStyles = createStyles(({ token, css }) => ({
  container: css`
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
  `,
  content: css`
    margin-bottom: 2rem;
  `,
  feedback: css`
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
  `,
  refinement: css`
    margin-top: 2rem;
  `,
}));

const mockResult = {
  content:
    "This is a sample generated content. It demonstrates how the results would look like in a real application. The content is formatted and styled according to the selected preferences.",
  metadata: {
    tone: "Professional",
    format: "Blog Post",
    platform: "LinkedIn",
    timestamp: new Date().toISOString(),
  },
};

export default function ResultsPage() {
  const { styles } = useStyles();
  const [result, setResult] = useState<GeneratedResult>(mockResult);
  const [refinementPrompt, setRefinementPrompt] = useState("");
  const [loading, setLoading] = useState(false);

  const handleRefinement = async () => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      setResult({
        ...result,
        content: `Refined content based on: "${refinementPrompt}"\n\n${result.content}`,
        metadata: {
          ...result.metadata,
          timestamp: new Date().toISOString(),
        },
      });
      setRefinementPrompt("");
      setLoading(false);
    }, 1500);
  };

  const handleDownload = () => {
    const blob = new Blob([JSON.stringify(result, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "generated-content.json";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className={styles.container}>
      <Card
        title="Generated Content"
        extra={
          <Button icon={<Download />} onClick={handleDownload}>
            Download
          </Button>
        }
      >
        <div className={styles.content}>
          <Text>{result.content}</Text>
        </div>

        <div>
          <Space direction="vertical">
            <Text type="secondary">
              Generated for: {result.metadata.platform}
            </Text>
            <Text type="secondary">Tone: {result.metadata.tone}</Text>
            <Text type="secondary">Format: {result.metadata.format}</Text>
          </Space>
        </div>

        <div className={styles.feedback}>
          <Button icon={<ThumbsUp />}>Helpful</Button>
          <Button icon={<ThumbsDown />}>Not Helpful</Button>
        </div>

        <div className={styles.refinement}>
          <Title level={4}>Refine Result</Title>
          <Space.Compact style={{ width: "100%" }}>
            <TextArea
              value={refinementPrompt}
              onChange={(e) => setRefinementPrompt(e.target.value)}
              placeholder="Enter refinement prompt (e.g., 'Make it funnier')"
              autoSize={{ minRows: 2, maxRows: 6 }}
            />
            <Button
              type="primary"
              icon={<RefreshCw />}
              onClick={handleRefinement}
              loading={loading}
              disabled={!refinementPrompt.trim()}
            >
              Refine
            </Button>
          </Space.Compact>
        </div>
      </Card>
    </div>
  );
}
