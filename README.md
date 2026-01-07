# BMI Calculator for Alfred Workflow

身長と体重から理想体重やBMIを計算するAlfred Workflowスクリプト。

## 機能

- **身長のみ入力**: 理想体重、痩せ体重、肥満体重を表示
- **身長+体重入力**: BMI値と体格判定を表示

## インストール

1. このリポジトリをクローンまたはダウンロード
2. Alfred Workflowsを開く
3. 新しいBlank Workflowを作成
4. Script Filterを追加して以下のように設定:
   - **Keyword**: `bmi`
   - **Title**: BMI Calculator
   - **Subtext**: 身長(cm) または 身長(cm) 体重(kg)
   - **Language**: `/usr/bin/python3`
   - **Script**:
     ```bash
     python3 /path/to/bmi_calculator.py "{query}"
     ```
     (パスは実際の `bmi_calculator.py` の場所に置き換えてください)

## 使い方

### 身長のみ入力

Alfred で以下のように入力:
```
bmi 170
```

結果例:
```
理想: 63.6kg | 痩せ: 53.5kg | 肥満: 72.2kg
身長170cmの場合の各体重基準値
```

### 身長+体重入力

Alfred で以下のように入力:
```
bmi 170 65
```

結果例:
```
BMI: 22.5 (標準)
身長170cm 体重65kg
```

## BMI判定基準

日本肥満学会の基準に準拠:

| BMI | 判定 |
|-----|------|
| < 18.5 | 痩せ |
| 18.5 - 24.9 | 標準 |
| 25.0 - 29.9 | 肥満(1度) |
| 30.0 - 34.9 | 肥満(2度) |
| 35.0 - 39.9 | 肥満(3度) |
| ≥ 40.0 | 肥満(4度) |

## コマンドラインでのテスト

Alfred Workflowに組み込む前に、コマンドラインでテストできます:

```bash
# 身長のみ
python3 bmi_calculator.py "170"

# 身長+体重
python3 bmi_calculator.py "170 65"

# JSON形式の確認
python3 bmi_calculator.py "170 65" | jq .
```

## 技術仕様

- **言語**: Python 3.9.6 (macOS標準)
- **依存関係**: なし (標準ライブラリのみ)
- **出力形式**: Alfred Script Filter JSON形式

## ライセンス

MIT License

## 参考資料

- [Alfred Script Filter Documentation](https://www.alfredapp.com/help/workflows/inputs/script-filter/)
- [Alfred Script Filter JSON Format](https://www.alfredapp.com/help/workflows/inputs/script-filter/json/)
