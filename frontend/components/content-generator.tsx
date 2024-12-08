// components/content-generator.tsx
'use client';

import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, Form, message, Modal, Select, Space, Spin } from 'antd';
import { createStyles } from 'antd-style';
import { RefreshCw, Wand2 } from 'lucide-react';
import React, { useEffect, useState } from 'react';
import { TrendingTopics } from './trending-topics';

// API response types
interface PromptResponse {
  prompt: string;
  link: string;
}

interface TextResponse {
  text: string;
}

interface MediaResponse {
  url: string;
}

interface RefineResponse {
  prompt: string;
}

interface TrendingResponse {
  topics: string[];
}

// Form values type
interface FormValues {
  input: string;
  tone: string;
  platform: string;
  trending?: string;
  outputType: OutputType;
}

// Output type
type OutputType = 'text' | 'meme' | 'video' | 'image';

// Generated content type
type GeneratedContent = string | null;

// Option type
interface Option {
  value: string;
  label: string;
}

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

const toneOptions: Option[] = [
  { value: 'professional', label: 'Professional' },
  { value: 'casual', label: 'Casual' },
  { value: 'humorous', label: 'Humorous' },
  { value: 'formal', label: 'Formal' },
];

const platformOptions: Option[] = [
  { value: 'news', label: 'News' },
  { value: 'twitter', label: 'Twitter' },
  { value: 'linkedin', label: 'LinkedIn' },
  { value: 'facebook', label: 'Facebook' },
];

const outputTypeOptions: Option[] = [
  { value: 'text', label: 'Text' },
  { value: 'meme', label: 'Meme' },
  { value: 'video', label: 'Video' },
  { value: 'image', label: 'Image' },
];

const useStyles = createStyles(({ token, css }) => ({
  container: css`
    opacity: 0;
    transition: opacity 0.3s ease-in;
    &.loaded {
      opacity: 1;
    }
  `,
  loadingContainer: css`
    width: 100%;
    height: 60vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: ${token.colorBgContainer};
  `,
  formContainer: css`
    .ant-form-item {
      margin-bottom: 24px;
    }
  `,
  formGrid: css`
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;

    @media (max-width: 1024px) {
      grid-template-columns: repeat(2, 1fr);
    }

    @media (max-width: 640px) {
      grid-template-columns: 1fr;
    }

    .ant-form-item {
      margin: 0;
    }
  `,
  previewContainer: css`
    margin-top: 32px;
    border-radius: ${token.borderRadiusLG}px;
    overflow: hidden;
  `,
  contentHeader: css`
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
  `,
  mediaPreview: css`
    aspect-ratio: 16/9;
    background: ${token.colorBgContainer};
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    border-radius: ${token.borderRadius}px;

    img,
    video {
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
    }
  `,
  sourceLink: css`
    margin-top: 16px;
    padding: 16px;
    background: ${token.colorBgContainer};
    border-radius: ${token.borderRadius}px;
    border: 1px solid ${token.colorBorder};
  `,
}));

export default function ContentGenerator() {
  const { styles } = useStyles();
  const [form] = Form.useForm<FormValues>();
  const [loading, setLoading] = useState<boolean>(false);
  const [initialLoading, setInitialLoading] = useState<boolean>(true);
  const [generatedContent, setGeneratedContent] =
    useState<GeneratedContent>(null);
  const [sourceLink, setSourceLink] = useState<string>('');
  const [outputType, setOutputType] = useState<OutputType>('text');
  const [isRefineModalOpen, setIsRefineModalOpen] = useState<boolean>(false);
  const [refineInput, setRefineInput] = useState<string>('');
  const [refining, setRefining] = useState<boolean>(false);
  const [lastPrompt, setLastPrompt] = useState<string>('');
  const [trendingTopics, setTrendingTopics] = useState<Option[]>([]);
  const [loadingTopics, setLoadingTopics] = useState<boolean>(true);

  useEffect(() => {
    const initializeComponent = async () => {
      try {
        form.resetFields();
        sessionStorage.removeItem('contentGeneratorInput');

        const response = await fetch(`${API_BASE_URL}/trending`);
        if (!response.ok) {
          throw new Error('Failed to fetch trending topics');
        }
        const data: TrendingResponse = await response.json();
        setTrendingTopics(
          data.topics.map((topic) => ({
            value: topic,
            label: topic,
          }))
        );
      } catch (error) {
        console.error('Failed to initialize:', error);
        message.error('Failed to load trending topics');
      } finally {
        setLoadingTopics(false);
        setTimeout(() => setInitialLoading(false), 300);
      }
    };

    initializeComponent();

    return () => {
      sessionStorage.removeItem('contentGeneratorInput');
    };
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    sessionStorage.setItem('contentGeneratorInput', e.target.value);
    form.setFieldsValue({ input: e.target.value });
  };

  const handleTopicClick = (topic: string) => {
    const currentInput = form.getFieldValue('input');
    const newInput = currentInput ? `${currentInput} #${topic}` : `#${topic}`;
    form.setFieldsValue({ input: newInput });
    sessionStorage.setItem('contentGeneratorInput', newInput);
  };

  const getPrompt = async (values: FormValues): Promise<PromptResponse> => {
    try {
      const requestData = {
        ...values,
        type: values.outputType,
      };

      const response = await fetch(`${API_BASE_URL}/get_prompt`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Failed to get prompt:', error);
      throw error;
    }
  };

  const generateContent = async (
    prompt: string,
    type: OutputType
  ): Promise<TextResponse | MediaResponse> => {
    try {
      const response = await fetch(`${API_BASE_URL}/generate_${type}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      message.error(`Failed to generate ${type}`);
      throw error;
    }
  };

  const handleRefine = async () => {
    if (!lastPrompt) {
      message.error('No content to refine');
      return;
    }

    setRefining(true);
    try {
      const refineResponse = await fetch(`${API_BASE_URL}/refine`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: lastPrompt,
          refine: refineInput,
        }),
      });

      if (!refineResponse.ok) {
        throw new Error('Failed to refine prompt');
      }

      const refinedPrompt: RefineResponse = await refineResponse.json();
      const result = await generateContent(refinedPrompt.prompt, outputType);

      if (outputType === 'text') {
        setGeneratedContent((result as TextResponse).text);
      } else {
        setGeneratedContent((result as MediaResponse).url);
      }

      setLastPrompt(refinedPrompt.prompt);
      setIsRefineModalOpen(false);
      setRefineInput('');
      message.success('Content refined successfully!');
    } catch (error) {
      console.error('Refinement failed:', error);
      message.error('Failed to refine content');
    } finally {
      setRefining(false);
    }
  };

  const handleSubmit = async (values: FormValues) => {
    setLoading(true);
    try {
      const promptResult = await getPrompt(values);
      setSourceLink(promptResult.link);
      setLastPrompt(promptResult.prompt);

      const result = await generateContent(promptResult.prompt, outputType);

      if (outputType === 'text') {
        setGeneratedContent((result as TextResponse).text);
      } else {
        setGeneratedContent((result as MediaResponse).url);
      }

      message.success('Content generated successfully!');
    } catch (error) {
      console.error('Generation failed:', error);
      message.error('Failed to generate content');
    } finally {
      setLoading(false);
    }
  };

  const handleOutputTypeChange = (value: OutputType) => {
    setOutputType(value);
    setGeneratedContent(null);
  };

  if (initialLoading) {
    return (
      <div className={styles.loadingContainer}>
        <Spin size="large" tip="Loading..." />
      </div>
    );
  }

  return (
    <div className={`${styles.container} ${!initialLoading ? 'loaded' : ''}`}>
      <Card className="w-full max-w-4xl mx-auto mt-8">
        <Form<FormValues>
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          className={styles.formContainer}
          disabled={loading}
        >
          <Form.Item
            name="input"
            label="What would you like to generate?"
            rules={[
              { required: true, message: 'Please enter your content prompt' },
            ]}
          >
            <Textarea
              onChange={handleInputChange}
              placeholder="Enter your content prompt here..."
              className="min-h-[100px]"
            />
          </Form.Item>

          <TrendingTopics
            topics={trendingTopics.map((t) => t.label)}
            onTopicClick={handleTopicClick}
          />

          <div className={styles.formGrid}>
            <Form.Item
              name="tone"
              label="Tone"
              rules={[{ required: true }]}
              className="m-0"
            >
              <Select<string>
                options={toneOptions}
                placeholder="Select tone"
                className="w-full"
              />
            </Form.Item>

            <Form.Item
              name="platform"
              label="Platform"
              rules={[{ required: true }]}
              className="m-0"
            >
              <Select<string>
                options={platformOptions}
                placeholder="Select platform"
                className="w-full"
              />
            </Form.Item>

            <Form.Item
              name="outputType"
              label="Output Format"
              rules={[{ required: true }]}
              className="m-0"
            >
              <Select<OutputType>
                options={outputTypeOptions}
                placeholder="Select output format"
                onChange={handleOutputTypeChange}
                className="w-full"
              />
            </Form.Item>
          </div>

          <Form.Item>
            <Button type="submit" disabled={loading} className="w-full">
              <Wand2 className="mr-2 h-4 w-4" />
              {loading ? 'Generating...' : 'Generate Content'}
            </Button>
          </Form.Item>
        </Form>

        {generatedContent && (
          <div className={styles.previewContainer}>
            <div className={styles.contentHeader}>
              <h3 className="text-lg font-semibold">Generated Content</h3>
              <Button
                size="sm"
                variant="outline"
                onClick={() => setIsRefineModalOpen(true)}
                className="flex items-center gap-2"
                disabled={refining}
              >
                <RefreshCw className="h-4 w-4" />
                Refine
              </Button>
            </div>

            {outputType === 'text' ? (
              <div className="p-4 bg-muted rounded-lg">
                <p className="whitespace-pre-wrap">{generatedContent}</p>
              </div>
            ) : (
              <div className={styles.mediaPreview}>
                {outputType === 'video' ? (
                  <video
                    src={generatedContent}
                    controls
                    className="w-full h-full"
                  />
                ) : (
                  <img
                    src={generatedContent}
                    alt="Generated content"
                    className="w-full h-full object-contain"
                  />
                )}
              </div>
            )}

            {sourceLink && (
              <div className={styles.sourceLink}>
                <div className="text-sm">
                  <span className="text-muted-foreground">Source: </span>
                  <a
                    href={sourceLink}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-primary hover:underline"
                  >
                    {sourceLink}
                  </a>
                </div>
              </div>
            )}
          </div>
        )}
      </Card>

      <Modal
        title="Refine Content"
        open={isRefineModalOpen}
        onCancel={() => {
          setIsRefineModalOpen(false);
          setRefineInput('');
        }}
        footer={[
          <Button
            key="cancel"
            variant="outline"
            onClick={() => {
              setIsRefineModalOpen(false);
              setRefineInput('');
            }}
          >
            Cancel
          </Button>,
          <Button
            key="submit"
            onClick={handleRefine}
            disabled={!refineInput.trim() || refining}
          >
            {refining ? 'Refining...' : 'Refine'}
          </Button>,
        ]}
      >
        <div className="my-4">
          <Textarea
            value={refineInput}
            onChange={(e) => setRefineInput(e.target.value)}
            placeholder="Enter your refinement instructions..."
            className="min-h-[100px]"
          />
          <p className="mt-2 text-sm text-muted-foreground">
            Describe how you'd like to refine the generated content.
          </p>
        </div>
      </Modal>
    </div>
  );
}
