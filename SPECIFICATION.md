# BMI計算 Alfred Workflow 仕様書

## 1. プロジェクト概要

身長と体重から理想体重やBMIを計算し、Alfred Workflow経由で結果を表示するスクリプト。

## 2. 技術仕様

### 2.1 基盤
- Alfred Workflow Script Filter

### 2.2 実装言語・環境
- Python 3.9.6
- 外部ライブラリ不使用
- 単一ファイル実装

### 2.3 入力仕様
- 入力元: `sys.argv[1:]`
- 入力パターン:
  - パターン0: `` (空入力)
  - パターン1: `身長` (cm単位、例: 170)
  - パターン2: `身長 体重` (スペース区切り、体重はkg単位、例: 170 65)

### 2.4 出力仕様

#### 2.4.1 出力形式
- JSON形式 (Alfred Script Filter JSON Format)
- 基本構造:
```json
{
  "items": [
    {
      "title": "計算結果",
      "subtitle": "補足情報",
      "arg": "引数（オプション）"
    }
  ]
}
```

#### 2.4.2 出力パターン

**パターン0: 入力なし（空入力）**
- items配列に1つのitem
- titleに使用方法を表示: `"身長(cm) を入力してください"`
- subtitleに使用方法を表示: `"身長(cm) を入力してください"`

**パターン1: 身長のみ入力時**
- items配列に1つのitem
- titleに理想体重、痩せ体重、肥満体重を表示
  - 表示形式: `"身長: Hcm, 痩せ: Xkg, 理想: Ykg, 肥満: Zkg"`
- subtitleに次のステップを表示: `"体重(kg) を入力してください"`

**パターン2: 身長と体重を入力時**
- items配列に1つのitem
- titleにBMI値と体格判定を表示
  - 表示形式: `"身長: Hcm, 体重: Wkg, BMI: X.X (カテゴリー)"`
- subtitleは空文字列: `""`

## 3. 機能要件

### 3.1 身長のみ入力時の計算項目
1. **理想体重 (標準体重)** - BMI 22の体重
   - 計算式: `身長(m)² × 22`
2. **痩せ体重** - BMI 18.5の体重
   - 計算式: `身長(m)² × 18.5`
3. **肥満体重** - BMI 25の体重
   - 計算式: `身長(m)² × 25`

### 3.2 身長と体重入力時の計算項目
1. **BMI値**
   - 計算式: `体重(kg) ÷ 身長(m)²`
2. **体格判定**
   - BMI < 18.5: 痩せ
   - 18.5 ≤ BMI < 25: 標準
   - 25 ≤ BMI < 30: 肥満(1度)
   - 30 ≤ BMI < 35: 肥満(2度)
   - 35 ≤ BMI < 40: 肥満(3度)
   - 40 ≤ BMI: 肥満(4度)

## 4. エラーハンドリング

### 4.1 入力検証
- 引数が0個または空文字の場合: 使用方法を表示（パターン0）
- 引数が3個以上の場合: エラーメッセージを表示
- 数値変換エラー: エラーメッセージを表示
- 身長が0以下または300cm超: 検証エラーメッセージを表示
- 体重が0以下または500kg超: 検証エラーメッセージを表示

### 4.2 エラー出力形式
```json
{
  "items": [
    {
      "title": "エラー内容",
      "subtitle": "使用方法の説明"
    }
  ]
}
```

### 4.3 重要な制約
- **stdoutへの出力制限**: 最終的なJSON以外は一切stdoutに出力しないこと（デバッグ出力、中間結果など禁止）
- **例外処理**: すべての例外をキャッチし、JSON形式でエラーメッセージを返すこと
- **言語**: すべてのエラーメッセージは日本語で表示すること

## 5. 出力例

### 5.0 入力なし（空入力）
```json
{
  "items": [
    {
      "title": "身長(cm) を入力してください",
      "subtitle": "身長(cm) を入力してください"
    }
  ]
}
```

### 5.1 身長のみ入力時 (例: 170cm)
```json
{
  "items": [
    {
      "title": "身長: 170cm, 痩せ: 53.5kg, 理想: 63.6kg, 肥満: 71.8kg",
      "subtitle": "体重(kg) を入力してください"
    }
  ]
}
```

### 5.2 身長と体重入力時 (例: 170cm 65kg)
```json
{
  "items": [
    {
      "title": "身長: 170cm, 体重: 65kg, BMI: 22.5 (標準)",
      "subtitle": ""
    }
  ]
}
```

### 5.3 エラー時 (例: 無効な入力)
```json
{
  "items": [
    {
      "title": "入力エラー",
      "subtitle": "使用方法: 身長(cm) または 身長(cm) 体重(kg)"
    }
  ]
}
```

## 6. ファイル構成

```
project/
├── SPECIFICATION.md      # 本仕様書
├── CLAUDE.md             # Claude Code用のガイドライン
├── .cursorrules          # Cursor AI用のプロジェクトルール
├── bmi_calculator.py     # メインスクリプト
├── README.md             # 使用方法とインストール手順（日本語）
└── .vscode/              # VSCode/Cursor設定
    ├── settings.json     # エディター設定
    ├── extensions.json   # 推奨拡張機能
    └── launch.json       # デバッグ構成
```

## 7. Alfred Workflow設定

### 7.1 Script Filter設定項目
- **Keyword**: `bmi` (推奨)
- **Argument**: Optional または Required
- **Language**: /usr/bin/python3
- **Script**: `python3 bmi_calculator.py "{query}"`

### 7.2 フロー
1. ユーザーがAlfredで `bmi 170` または `bmi 170 65` と入力
2. Script Filterがスクリプトを実行
3. JSON結果がAlfredに表示される

## 8. 参考資料
- [Alfred Script Filter Documentation](https://www.alfredapp.com/help/workflows/inputs/script-filter/)
- [Alfred Script Filter JSON Format](https://www.alfredapp.com/help/workflows/inputs/script-filter/json/)
- BMI基準: 日本肥満学会の基準に準拠
- CLAUDE.md: Claude Code用の実装ガイドライン
- .cursorrules: Cursor AI用のプロジェクトルール
