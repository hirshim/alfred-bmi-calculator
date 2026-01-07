#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BMI Calculator for Alfred Workflow
Calculates ideal weight and BMI based on height and weight inputs.
"""

import sys
import json


def create_output(title, subtitle):
    """Create Alfred Script Filter JSON output."""
    return json.dumps({
        "items": [
            {
                "title": title,
                "subtitle": subtitle,
                "arg": title
            }
        ]
    }, ensure_ascii=False)


def calculate_weights(height_cm):
    """Calculate ideal, underweight, and obese weights for given height."""
    height_m = height_cm / 100
    height_squared = height_m ** 2

    ideal_weight = height_squared * 22
    underweight = height_squared * 18.5
    obese_weight = height_squared * 25

    return ideal_weight, underweight, obese_weight


def calculate_bmi(height_cm, weight_kg):
    """Calculate BMI and return category."""
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    if bmi < 18.5:
        category = "痩せ"
    elif bmi < 25:
        category = "標準"
    elif bmi < 30:
        category = "肥満(1度)"
    elif bmi < 35:
        category = "肥満(2度)"
    elif bmi < 40:
        category = "肥満(3度)"
    else:
        category = "肥満(4度)"

    return bmi, category


def main():
    """Main function to process input and generate output."""
    # Get input from command line arguments
    if len(sys.argv) < 2:
        print(create_output(
            "身長(cm) を入力してください",
            "身長(cm) を入力してください"
        ))
        return

    # Parse input - Alfred passes the query as a single argument
    query = sys.argv[1].strip()

    if not query:
        print(create_output(
            "身長(cm) を入力してください",
            "身長(cm) を入力してください"
        ))
        return

    # Split by whitespace
    parts = query.split()

    try:
        if len(parts) == 1:
            # Height only - show ideal weight ranges
            height = float(parts[0])

            # Validate height
            if height <= 0 or height > 300:
                print(create_output(
                    "入力エラー",
                    "身長は1〜300cmの範囲で入力してください"
                ))
                return

            ideal, underweight, obese = calculate_weights(height)

            title = f"身長: {height:.0f}cm, 痩せ: {underweight:.1f}kg, 理想: {ideal:.1f}kg, 肥満: {obese:.1f}kg"
            subtitle = "体重(kg) を入力してください"

            print(create_output(title, subtitle))

        elif len(parts) == 2:
            # Height and weight - calculate BMI
            height = float(parts[0])
            weight = float(parts[1])

            # Validate inputs
            if height <= 0 or height > 300:
                print(create_output(
                    "入力エラー",
                    "身長は1〜300cmの範囲で入力してください"
                ))
                return

            if weight <= 0 or weight > 500:
                print(create_output(
                    "入力エラー",
                    "体重は1〜500kgの範囲で入力してください"
                ))
                return

            bmi, category = calculate_bmi(height, weight)

            title = f"身長: {height:.0f}cm, 体重: {weight:.0f}kg, BMI: {bmi:.1f} ({category})"
            subtitle = ""

            print(create_output(title, subtitle))

        else:
            # Too many arguments
            print(create_output(
                "入力エラー",
                "使用方法: 身長(cm) または 身長(cm) 体重(kg)"
            ))

    except ValueError:
        print(create_output(
            "入力エラー",
            "数値を正しく入力してください (例: 170 または 170 65)"
        ))
    except Exception as e:
        print(create_output(
            "エラーが発生しました",
            f"エラー内容: {str(e)}"
        ))


if __name__ == "__main__":
    main()
