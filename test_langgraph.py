#!/usr/bin/env python3
"""
LangGraph AI 어댑터 테스트 스크립트
"""
import requests
import time

def test_langgraph_api():
    """LangGraph AI API 테스트"""
    print("🔍 LangGraph AI 어댑터 테스트 시작")
    print("=" * 50)
    
    # 1. 헬스 체크
    print("\n1️⃣ 헬스 체크")
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"상태: {response.status_code}")
        if response.status_code == 200:
            print("✅ 서버 정상")
        else:
            print("❌ 서버 오류")
            return
    except Exception as e:
        print(f"❌ 서버 연결 실패: {e}")
        return
    
    # 2. 기본 질문 테스트
    print("\n2️⃣ 기본 AI 질문 테스트")
    try:
        response = requests.post(
            "http://localhost:8000/api/chat",
            headers={"Content-Type": "application/json"},
            json={
                "question": "안녕하세요! LangGraph AI 테스트입니다.",
                "temperature": 0.7,
                "max_tokens": 100
            }
        )
        print(f"상태: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"답변: {result['answer'][:100]}...")
            print(f"사용량: {result['usage']}")
        else:
            print(f"❌ API 오류: {response.text}")
    except Exception as e:
        print(f"❌ 요청 실패: {e}")
    
    # 3. 복잡한 질문 테스트
    print("\n3️⃣ 복잡한 AI 질문 테스트")
    try:
        response = requests.post(
            "http://localhost:8000/api/chat",
            headers={"Content-Type": "application/json"},
            json={
                "question": "인공지능의 미래에 대해 설명해주세요. 특히 LangGraph와 LangChain의 역할에 대해 자세히 알려주세요.",
                "temperature": 0.5,
                "max_tokens": 200
            }
        )
        print(f"상태: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"답변 길이: {len(result['answer'])} 문자")
            print(f"답변: {result['answer'][:150]}...")
        else:
            print(f"❌ API 오류: {response.text}")
    except Exception as e:
        print(f"❌ 요청 실패: {e}")
    
    print("\n" + "=" * 50)
    print("✅ LangGraph AI 테스트 완료")

if __name__ == "__main__":
    test_langgraph_api() 