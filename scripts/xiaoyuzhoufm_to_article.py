#!/usr/bin/env python3
"""
小宇宙FM播客转文章工具
将小宇宙FM链接转换为自然流畅的文章
"""

import re
import json
import subprocess
import sys

def extract_episode_id(url):
    """从URL中提取episode ID"""
    patterns = [
        r'xiaoyuzhoufm\.com/episode/([a-zA-Z0-9]+)',
        r'xiaoyuz\.com/episode/([a-zA-Z0-9]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def fetch_content(url):
    """使用 jina.ai 获取页面内容"""
    jina_url = f"https://r.jina.ai/{url}"
    try:
        result = subprocess.run(
            ['curl', '-s', '--max-time', '30', jina_url],
            capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error fetching content: {e}", file=sys.stderr)
        return None

def parse_content(raw_content):
    """解析抓取的内容，提取关键信息"""
    # 提取标题
    title_match = re.search(r'^Title:\s*(.+)$', raw_content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "未知标题"
    
    # 提取播客名称
    podcast_match = re.search(r'\[([^\]]+)\]', raw_content)
    podcast_name = podcast_match.group(1) if podcast_match else "未知播客"
    
    # 提取时长
    duration_match = re.search(r'(\d+分钟)', raw_content)
    duration = duration_match.group(1) if duration_match else "未知时长"
    
    # 提取Transcript (Markdown Content之后的内容)
    transcript_section = ""
    if "Markdown Content:" in raw_content:
        transcript_section = raw_content.split("Markdown Content:")[1]
    
    # 清理内容
    transcript_section = re.sub(r'!\[Image[^\]]*\]\([^)]+\)', '', transcript_section)
    transcript_section = re.sub(r'\n{3,}', '\n\n', transcript_section)
    transcript_section = transcript_section.strip()
    
    return {
        'title': title,
        'podcast_name': podcast_name,
        'duration': duration,
        'content': transcript_section,
        'url': ''
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python xiaoyuzhoufm_to_article.py <xiaoyuzhoufm_url>", file=sys.stderr)
        sys.exit(1)
    
    url = sys.argv[1]
    
    # 提取episode ID
    episode_id = extract_episode_id(url)
    if not episode_id:
        print("Error: Invalid Xiaoyu Zhou FM URL", file=sys.stderr)
        sys.exit(1)
    
    print(f"🔍 Fetching episode: {episode_id}", file=sys.stderr)
    
    # 抓取内容
    raw_content = fetch_content(url)
    if not raw_content:
        print("Error: Failed to fetch content", file=sys.stderr)
        sys.exit(1)
    
    # 解析内容
    parsed_data = parse_content(raw_content)
    parsed_data['url'] = url
    
    # 输出JSON供模型使用
    print(json.dumps(parsed_data, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
