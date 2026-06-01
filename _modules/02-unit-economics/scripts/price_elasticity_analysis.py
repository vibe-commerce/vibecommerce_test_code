"""
Анализ ценовой эластичности спроса по данным продаж.
Источник: sales_data_v1.0.xlsx (50 SKU × 2 платформы × 12 недель)

Эластичность спроса по цене: E = (ΔQ/Q̄) / (ΔP/P̄)
  E < -1  → эластичный спрос (цена вниз → выручка вверх)
  E > -1  → неэластичный спрос (цена вниз → выручка вниз)
  E = -1  → единичная эластичность
"""

import openpyxl
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
import os

# ── Настройки ──
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['figure.dpi'] = 150

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, 'sales_data_v1.0.xlsx')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'analysis_output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Загрузка данных ──
wb = openpyxl.load_workbook(DATA_FILE, data_only=True)
ws = wb['Продажи']

# Структура: {(sku, name, category): {price: [qty1, qty2, ...]}}
sku_price_qty = defaultdict(lambda: defaultdict(list))
sku_platform_data = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

for row in ws.iter_rows(min_row=2, values_only=True):
    week, sku, name, cat, platform, qty, price = row[0], row[1], row[2], row[3], row[4], row[5], row[6]
    if qty is not None and price is not None and qty > 0:
        sku_price_qty[(sku, name, cat)][price].append(qty)
        sku_platform_data[(sku, name, cat)][platform][price].append(qty)

# ── Расчёт эластичности ──
# Метод средней точки (arc elasticity): E = ((Q2-Q1)/((Q2+Q1)/2)) / ((P2-P1)/((P2+P1)/2))
results = []

for (sku, name, cat), price_data in sorted(sku_price_qty.items()):
    prices = sorted(price_data.keys())
    if len(prices) < 2:
        continue

    # Средние продажи на каждом ценовом уровне
    avg_qty_by_price = {p: sum(qs) / len(qs) for p, qs in price_data.items()}

    # Считаем эластичность между мин и макс ценой
    p_low, p_high = prices[0], prices[-1]
    q_low, q_high = avg_qty_by_price[p_low], avg_qty_by_price[p_high]

    # Средняя точка
    p_avg = (p_low + p_high) / 2
    q_avg = (q_low + q_high) / 2

    if p_avg == 0 or q_avg == 0:
        continue

    elasticity = ((q_high - q_low) / q_avg) / ((p_high - p_low) / p_avg)

    # Средняя выручка
    total_qty = sum(sum(qs) for qs in price_data.values())
    total_rev = sum(p * sum(qs) for p, qs in price_data.items())
    avg_price = total_rev / total_qty if total_qty > 0 else 0

    results.append({
        'sku': sku,
        'name': name,
        'category': cat,
        'p_low': p_low,
        'p_high': p_high,
        'q_at_low': q_low,
        'q_at_high': q_high,
        'elasticity': elasticity,
        'total_qty': total_qty,
        'total_rev': total_rev,
        'avg_price': avg_price,
        'price_delta_pct': (p_high - p_low) / p_low * 100,
    })

# Сортируем по эластичности
results.sort(key=lambda x: x['elasticity'])

# ── Печать таблицы ──
print("=" * 110)
print(f"{'SKU':>4} {'Название':<38} {'Категория':<18} {'Цена ↓':>7} {'Цена ↑':>7} {'ΔP%':>5} {'Q↓':>5} {'Q↑':>5} {'E':>7} {'Тип':<12}")
print("=" * 110)

for r in results:
    e = r['elasticity']
    if e < -1:
        etype = "ЭЛАСТИЧН."
    elif e > -0.5:
        etype = "НЕЭЛАСТИЧН."
    else:
        etype = "~ЕДИНИЧН."

    print(f"{r['sku']:>4} {r['name']:<38} {r['category']:<18} {r['p_low']:>7.0f} {r['p_high']:>7.0f} "
          f"{r['price_delta_pct']:>4.1f}% {r['q_at_low']:>5.1f} {r['q_at_high']:>5.1f} {e:>7.2f} {etype:<12}")

# ── ГРАФИК 1: Барчарт эластичности по всем товарам ──
fig, ax = plt.subplots(figsize=(16, 14))

names_short = [f"SKU{r['sku']} {r['name'][:25]}" for r in results]
elasticities = [r['elasticity'] for r in results]
colors = ['#d32f2f' if e < -1 else '#388e3c' if e > -0.5 else '#f57c00' for e in elasticities]

bars = ax.barh(range(len(results)), elasticities, color=colors, height=0.7, edgecolor='white', linewidth=0.5)
ax.set_yticks(range(len(results)))
ax.set_yticklabels(names_short, fontsize=8)
ax.axvline(x=-1, color='red', linestyle='--', alpha=0.5, label='E = -1 (граница эластичности)')
ax.axvline(x=0, color='gray', linestyle='-', alpha=0.3)
ax.set_xlabel('Эластичность спроса по цене (E)')
ax.set_title('Ценовая эластичность спроса по всем товарам\n(данные: WB + Ozon, нояб 2025 – фев 2026)', fontsize=14, fontweight='bold')
ax.legend(loc='lower right')
ax.invert_yaxis()

# Аннотация зон
ax.text(-3.5, -1.5, '← ЭЛАСТИЧНЫЙ спрос\n(снижение цены → рост выручки)',
        fontsize=9, color='#d32f2f', ha='center', style='italic')
ax.text(0.5, -1.5, 'НЕЭЛАСТ. →\n(цена мало влияет)',
        fontsize=9, color='#388e3c', ha='center', style='italic')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '01_elasticity_all_skus.png'), bbox_inches='tight')
plt.close()
print(f"\n✅ Сохранён: {OUTPUT_DIR}/01_elasticity_all_skus.png")

# ── ГРАФИК 2: Эластичность по категориям (средняя) ──
cat_elast = defaultdict(list)
for r in results:
    cat_elast[r['category']].append(r['elasticity'])

categories = sorted(cat_elast.keys(), key=lambda c: sum(cat_elast[c]) / len(cat_elast[c]))
cat_means = [sum(cat_elast[c]) / len(cat_elast[c]) for c in categories]
cat_mins = [min(cat_elast[c]) for c in categories]
cat_maxs = [max(cat_elast[c]) for c in categories]

fig, ax = plt.subplots(figsize=(12, 6))
colors_cat = ['#d32f2f' if m < -1 else '#388e3c' if m > -0.5 else '#f57c00' for m in cat_means]
bars = ax.barh(categories, cat_means, color=colors_cat, height=0.6, edgecolor='white')

# Разброс
for i, (cat, mn, mx) in enumerate(zip(categories, cat_mins, cat_maxs)):
    ax.plot([mn, mx], [i, i], color='gray', linewidth=2, alpha=0.5)
    ax.plot(mn, i, 'o', color='gray', markersize=4, alpha=0.5)
    ax.plot(mx, i, 'o', color='gray', markersize=4, alpha=0.5)

ax.axvline(x=-1, color='red', linestyle='--', alpha=0.5, label='E = -1')
ax.set_xlabel('Средняя эластичность (E)')
ax.set_title('Эластичность спроса по категориям\n(среднее ± разброс по SKU)', fontsize=14, fontweight='bold')
ax.legend()

for bar, val in zip(bars, cat_means):
    ax.text(val - 0.1, bar.get_y() + bar.get_height() / 2, f'{val:.2f}',
            va='center', ha='right', fontsize=10, fontweight='bold', color='white')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '02_elasticity_by_category.png'), bbox_inches='tight')
plt.close()
print(f"✅ Сохранён: {OUTPUT_DIR}/02_elasticity_by_category.png")

# ── ГРАФИК 3: Scatter — цена vs объём продаж (ТОП-12 товаров по продажам) ──
top12 = sorted(results, key=lambda x: x['total_qty'], reverse=True)[:12]

fig, axes = plt.subplots(3, 4, figsize=(18, 12))
axes = axes.flatten()

for idx, r in enumerate(top12):
    ax = axes[idx]
    sku_key = (r['sku'], r['name'], r['category'])

    # Данные по платформам
    for platform, marker, color in [('WB', 'o', '#7b1fa2'), ('Ozon', 's', '#1565c0')]:
        if platform in sku_platform_data[sku_key]:
            pdata = sku_platform_data[sku_key][platform]
            xs, ys = [], []
            for price, qtys in pdata.items():
                for q in qtys:
                    xs.append(price)
                    ys.append(q)
            ax.scatter(xs, ys, marker=marker, color=color, alpha=0.6, s=40, label=platform)

    e = r['elasticity']
    ecolor = '#d32f2f' if e < -1 else '#388e3c' if e > -0.5 else '#f57c00'
    ax.set_title(f"SKU{r['sku']}: {r['name'][:22]}\nE = {e:.2f}", fontsize=9, color=ecolor, fontweight='bold')
    ax.set_xlabel('Цена, ₽', fontsize=8)
    ax.set_ylabel('Продажи, шт', fontsize=8)
    ax.tick_params(labelsize=7)
    ax.legend(fontsize=7, loc='best')
    ax.grid(True, alpha=0.2)

fig.suptitle('Цена vs Объём продаж — ТОП-12 товаров\n(каждая точка = 1 неделя на площадке)',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '03_price_vs_qty_top12.png'), bbox_inches='tight')
plt.close()
print(f"✅ Сохранён: {OUTPUT_DIR}/03_price_vs_qty_top12.png")

# ── ГРАФИК 4: Кривая спроса для нескольких товаров с 3+ ценовыми уровнями ──
multi_price_skus = [r for r in results if len(sku_price_qty[(r['sku'], r['name'], r['category'])]) >= 3]

if multi_price_skus:
    fig, axes = plt.subplots(2, 4, figsize=(18, 8))
    axes = axes.flatten()

    for idx, r in enumerate(multi_price_skus[:8]):
        ax = axes[idx]
        sku_key = (r['sku'], r['name'], r['category'])
        price_data = sku_price_qty[sku_key]

        prices_sorted = sorted(price_data.keys())
        avg_qtys = [sum(price_data[p]) / len(price_data[p]) for p in prices_sorted]
        revenues = [p * q for p, q in zip(prices_sorted, avg_qtys)]

        # Кривая спроса
        ax.plot(prices_sorted, avg_qtys, 'o-', color='#1565c0', linewidth=2, markersize=8, label='Спрос (шт)')

        # Выручка на 2й оси
        ax2 = ax.twinx()
        ax2.bar(prices_sorted, revenues, width=(prices_sorted[-1] - prices_sorted[0]) * 0.15,
                alpha=0.3, color='#388e3c', label='Выручка')
        ax2.set_ylabel('Выручка, ₽', fontsize=8, color='#388e3c')
        ax2.tick_params(axis='y', labelsize=7, labelcolor='#388e3c')

        e = r['elasticity']
        ecolor = '#d32f2f' if e < -1 else '#388e3c' if e > -0.5 else '#f57c00'
        ax.set_title(f"SKU{r['sku']}: {r['name'][:22]}\nE = {e:.2f}", fontsize=9, color=ecolor, fontweight='bold')
        ax.set_xlabel('Цена, ₽', fontsize=8)
        ax.set_ylabel('Ср. продажи, шт/нед', fontsize=8, color='#1565c0')
        ax.tick_params(labelsize=7, axis='y', labelcolor='#1565c0')
        ax.tick_params(labelsize=7, axis='x')
        ax.grid(True, alpha=0.2)

    # Скрыть неиспользованные axes
    for idx in range(len(multi_price_skus[:8]), 8):
        axes[idx].set_visible(False)

    fig.suptitle('Кривые спроса — товары с 3+ ценовыми уровнями\n(средние продажи/нед на каждом уровне цены)',
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, '04_demand_curves_multi_price.png'), bbox_inches='tight')
    plt.close()
    print(f"✅ Сохранён: {OUTPUT_DIR}/04_demand_curves_multi_price.png")

# ── ГРАФИК 5: Матрица — ΔЦена% vs ΔСпрос% (все SKU) ──
fig, ax = plt.subplots(figsize=(12, 8))

for r in results:
    dp = r['price_delta_pct']
    dq = ((r['q_at_high'] - r['q_at_low']) / r['q_at_low']) * 100 if r['q_at_low'] > 0 else 0

    size = max(20, min(200, r['total_qty'] / 5))
    e = r['elasticity']
    color = '#d32f2f' if e < -1 else '#388e3c' if e > -0.5 else '#f57c00'
    ax.scatter(dp, dq, s=size, c=color, alpha=0.6, edgecolors='white', linewidth=0.5)

    # Подписи для крайних точек
    if abs(e) > 3 or abs(dq) > 50:
        ax.annotate(f"SKU{r['sku']}", (dp, dq), fontsize=7, alpha=0.7,
                   xytext=(5, 5), textcoords='offset points')

ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
ax.set_xlabel('Δ Цена, % (от мин к макс)', fontsize=11)
ax.set_ylabel('Δ Объём продаж, % (при макс цене vs мин цене)', fontsize=11)
ax.set_title('Чувствительность спроса: изменение цены vs изменение объёма\n(размер = объём продаж)', fontsize=14, fontweight='bold')

# Легенда
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#d32f2f', markersize=10, label='Эластичный (E < -1)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#f57c00', markersize=10, label='Ед. эластичность (-1 < E < -0.5)'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='#388e3c', markersize=10, label='Неэластичный (E > -0.5)'),
]
ax.legend(handles=legend_elements, loc='upper right')
ax.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '05_price_vs_demand_change.png'), bbox_inches='tight')
plt.close()
print(f"✅ Сохранён: {OUTPUT_DIR}/05_price_vs_demand_change.png")

# ── Итоговая статистика ──
elastic = [r for r in results if r['elasticity'] < -1]
inelastic = [r for r in results if r['elasticity'] > -0.5]
unit_elastic = [r for r in results if -1 <= r['elasticity'] <= -0.5]

print(f"\n{'=' * 60}")
print("ИТОГИ АНАЛИЗА ЭЛАСТИЧНОСТИ")
print(f"{'=' * 60}")
print(f"Всего SKU проанализировано: {len(results)}")
print(f"  🔴 Эластичный спрос (E < -1):     {len(elastic):>3} ({len(elastic)/len(results)*100:.0f}%)")
print(f"  🟠 Единичная эластичность:          {len(unit_elastic):>3} ({len(unit_elastic)/len(results)*100:.0f}%)")
print(f"  🟢 Неэластичный спрос (E > -0.5): {len(inelastic):>3} ({len(inelastic)/len(results)*100:.0f}%)")
print("\nСамые эластичные (чувствительны к цене):")
for r in results[:5]:
    print(f"  SKU{r['sku']:>2} {r['name']:<35} E = {r['elasticity']:.2f}")
print("\nСамые неэластичные (можно повышать цену):")
for r in results[-5:]:
    print(f"  SKU{r['sku']:>2} {r['name']:<35} E = {r['elasticity']:.2f}")

wb.close()
print(f"\n📁 Все графики сохранены в: {OUTPUT_DIR}/")
