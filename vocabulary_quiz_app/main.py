from __future__ import annotations

import tkinter as tk

from app import VocabularyQuizApp
from data import WORDS


def save_incorrect_words(incorrect_list: list[tuple[str, str]]) -> None:
    if not incorrect_list:
        print("\n🎉 모든 문제를 맞추셨습니다! 오답 노트가 생성되지 않습니다.")
        return
    try:
        with open("incorrect_words.txt", "w", encoding="utf-8") as f:
            f.write("=== [오답 노트] 틀린 단어 목록 ===\n")
            for word, meaning in incorrect_list:
                f.write(f"❌ 단어: {word} | 뜻: {meaning}\n")
        print("\n💾 틀린 단어가 'incorrect_words.txt' 파일에 저장되었습니다.")
    except Exception as e:
        print(f"\n⚠️ 파일 저장 중 오류 발생: {e}")


def print_final_stats(app: VocabularyQuizApp) -> None:
    total = app.total
    score = app.score
    if total == 0:
        print("\n📊 풀이한 문제가 없습니다.")
        return
    accuracy = score / total * 100
    print("\n" + "=" * 36)
    print("📊  최종 결과")
    print("=" * 36)
    print(f"  총 문제 수  : {total}문제")
    print(f"  정 답 수    : {score}문제")
    print(f"  오 답 수    : {total - score}문제")
    print(f"  정 답 률    : {accuracy:.1f}%")
    print("=" * 36)


def main() -> int:
    root = tk.Tk()
    app = VocabularyQuizApp(root, WORDS)
    root.mainloop()
    print_final_stats(app)
    save_incorrect_words(app.incorrect_words)
    return 0


if __name__ == "__main__":
    main()