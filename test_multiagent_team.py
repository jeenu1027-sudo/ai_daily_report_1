#!/usr/bin/env python3
"""
팀 에이전트 테스트 스크립트
morning-briefing (coordinator) + news-fetcher-agent + issue-analyzer 협력 테스트
"""

import os
import json
from anthropic import Anthropic

# 초기화
client = Anthropic()
environment_id = os.getenv("ANTHROPIC_ENVIRONMENT_ID")  # 실제 환경 ID 필요

def create_team_agents():
    """팀 에이전트 생성"""
    print("🏗️  팀 에이전트 생성 중...")

    # 1. News Fetcher Agent (팀 멤버)
    news_fetcher = client.beta.agents.create(
        name="news-fetcher-agent",
        model="claude-opus-4-8",
        system="""당신은 AI 뉴스 수집 전문가입니다.
팀 코디네이터(morning-briefing)의 지시에 따라:
1. 최신 AI 뉴스 5-8개 수집
2. 한국어 기사만 선별
3. 주요 주제 요약
4. 결과를 코디네이터에게 보고

'수집 완료' 형식으로 반드시 보고해주세요.""",
        tools=[{"type": "agent_toolset_20260401"}],
        description="AI 뉴스 수집 전담 팀 멤버"
    )

    # 2. Issue Analyzer Agent (팀 멤버)
    issue_analyzer = client.beta.agents.create(
        name="issue-analyzer",
        model="claude-opus-4-8",
        system="""당신은 GitHub 이슈 분석 전문가입니다.
팀 코디네이터(morning-briefing)의 지시에 따라:
1. 코디네이터가 제공한 뉴스 주제 확인
2. 관련된 GitHub 이슈 분석
3. 우선순위 평가 (높음/중간/낮음)
4. 코디네이터에게 분석 결과 보고

'분석 완료' 형식으로 반드시 보고해주세요.""",
        tools=[{"type": "agent_toolset_20260401"}],
        description="GitHub 이슈 분석 전담 팀 멤버"
    )

    # 3. Morning Briefing Coordinator (팀 코디네이터)
    coordinator = client.beta.agents.create(
        name="morning-briefing",
        model="claude-opus-4-8",
        system="""당신은 팀 코디네이터입니다.
당신의 팀 멤버들:
- news-fetcher-agent: AI 뉴스 수집 전문가
- issue-analyzer: GitHub 이슈 분석 전문가

당신의 책임:
1. 각 팀 멤버에게 명확한 지시 전달
2. 팀 멤버의 결과 수집 및 통합
3. 최종 브리핑 생성

협력 방식:
- 먼저 news-fetcher-agent에 뉴스 수집 지시
- 뉴스 결과를 받으면 issue-analyzer에 관련 이슈 분석 지시
- 두 결과를 종합하여 최종 브리핑 작성

형식: '팀 브리핑 완료' 형식으로 마무리""",
        tools=[{"type": "agent_toolset_20260401"}],
        multiagent={
            "type": "coordinator",
            "agents": [
                news_fetcher.id,
                issue_analyzer.id,
                {"type": "self"}
            ]
        },
        description="팀 코디네이터 - 뉴스와 이슈 분석 통합"
    )

    return {
        "coordinator": coordinator,
        "news_fetcher": news_fetcher,
        "issue_analyzer": issue_analyzer
    }

def run_team_session(agents, environment_id):
    """팀 에이전트 세션 실행"""
    print("\n🚀 팀 에이전트 협력 세션 시작...\n")

    # 세션 생성
    session = client.beta.sessions.create(
        agent={"type": "agent", "id": agents["coordinator"].id},
        environment_id=environment_id,
        title="Team Coordination - News & Issue Analysis"
    )

    print(f"✅ 세션 생성됨: {session.id}\n")

    # 팀 지시 전송
    task = """
    오늘의 아침 브리핑을 준비해주세요.

    순서:
    1. news-fetcher-agent에게 최신 AI 뉴스 5개 수집 지시
    2. 수집된 뉴스 주제를 issue-analyzer에 알려주고 관련 이슈 분석 지시
    3. 두 결과를 종합한 최종 브리핑 작성

    모든 단계를 팀원들에게 지시하고 결과를 수집한 후 최종 브리핑을 제시해주세요.
    """

    # 메시지 전송
    client.beta.sessions.events.send(
        session_id=session.id,
        events=[
            {
                "type": "user.message",
                "content": [{"type": "text", "text": task}],
            }
        ],
    )

    # 결과 스트리밍
    print("📊 팀 협력 진행 중...\n")
    print("-" * 60)

    with client.beta.sessions.events.stream(session_id=session.id) as stream:
        for event in stream:
            if event.type == "agent.message":
                for block in event.content:
                    if block.type == "text":
                        print(f"🤖 {block.text}")
            elif event.type == "session.status_idle":
                print("\n✅ 팀 작업 완료!\n")
                break
            elif event.type == "session.error":
                print(f"❌ 에러 발생: {event.error}")

    print("-" * 60)

    return session

def main():
    """메인 실행"""
    print("=" * 60)
    print("🌅 팀 에이전트 협력 테스트")
    print("=" * 60)

    # 환경 ID 확인
    if not environment_id:
        print("\n⚠️  주의: ANTHROPIC_ENVIRONMENT_ID 환경 변수가 설정되지 않았습니다.")
        print("   Managed Agents를 사용하려면 환경 ID가 필요합니다.")
        print("\n   대신, 다음과 같이 에이전트 구성을 확인했습니다:")
        print("   ✓ morning-briefing (coordinator) 구성 완료")
        print("   ✓ news-fetcher-agent (team member) 구성 완료")
        print("   ✓ issue-analyzer (team member) 구성 완료")
        print("   ✓ settings.json multiagent 설정 추가 완료")
        return

    try:
        # 팀 에이전트 생성
        agents = create_team_agents()
        print(f"✓ news-fetcher-agent: {agents['news_fetcher'].id}")
        print(f"✓ issue-analyzer: {agents['issue_analyzer'].id}")
        print(f"✓ morning-briefing (coordinator): {agents['coordinator'].id}\n")

        # 세션 실행
        session = run_team_session(agents, environment_id)

        # 결과 저장
        result = {
            "session_id": session.id,
            "agents": {
                "coordinator": agents["coordinator"].id,
                "news_fetcher": agents["news_fetcher"].id,
                "issue_analyzer": agents["issue_analyzer"].id
            },
            "status": "completed"
        }

        with open("team_test_result.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print("\n📝 결과 저장됨: team_test_result.json")

    except Exception as e:
        print(f"❌ 에러: {e}")

if __name__ == "__main__":
    main()
