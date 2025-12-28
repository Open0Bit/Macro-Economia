"""
Script 03: Analise de Sincronizacao Institucional
Framework: Preparacao Assimetrica e Crises Sistemicas
Autor: Gabriel W. Soares
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend nao-interativo
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
import os
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

def calculate_rolling_correlation():
    """Calcula correlacao rolling entre ETFs"""
    print("\n[1/4] Calculando correlacao rolling entre ETFs...")
    
    returns = pd.read_csv('data/processed/etf_returns.csv', 
                          index_col=0, parse_dates=True)
    
    china_etfs = ['FXI', 'MCHI', 'KWEB']
    available_etfs = [etf for etf in china_etfs if etf in returns.columns]
    
    if len(available_etfs) < 2:
        print(f"  [ERRO] ETFs insuficientes. Disponiveis: {available_etfs}")
        return None
    
    print(f"  ETFs analisados: {', '.join(available_etfs)}")
    
    window = 90
    correlations = {}
    
    for i, etf1 in enumerate(available_etfs):
        for etf2 in available_etfs[i+1:]:
            pair_name = f"{etf1}_{etf2}"
            rolling_corr = returns[etf1].rolling(window).corr(returns[etf2])
            correlations[pair_name] = rolling_corr
            print(f"  -> {pair_name}: corr media = {rolling_corr.mean():.3f}")
    
    df_corr = pd.DataFrame(correlations)
    df_corr['SYNC_INDEX'] = df_corr.mean(axis=1)
    
    output_path = 'data/processed/synchronization_index.csv'
    df_corr.to_csv(output_path)
    
    print(f"\n  [OK] Indice de sincronizacao calculado")
    print(f"  [OK] Salvo em {output_path}")
    
    return df_corr

def compare_periods():
    """Compara sincronizacao entre periodos"""
    print("\n[2/4] Comparando sincronizacao entre periodos...")
    
    sync = pd.read_csv('data/processed/synchronization_index.csv', 
                       index_col=0, parse_dates=True)
    
    stress = pd.read_csv('data/processed/stress_index.csv', 
                         index_col=0, parse_dates=True)
    
    common_index = sync.index.intersection(stress.index)
    sync_aligned = sync.loc[common_index, 'SYNC_INDEX']
    stress_aligned = stress.loc[common_index, 'STRESS_INDEX']
    
    stress_q75 = stress_aligned.quantile(0.75)
    stress_q25 = stress_aligned.quantile(0.25)
    
    high_stress = stress_aligned > stress_q75
    low_stress = stress_aligned < stress_q25
    
    sync_high_stress = sync_aligned[high_stress]
    sync_low_stress = sync_aligned[low_stress]
    
    print(f"\n  Periodo de ALTO estresse (Q4):")
    print(f"    Observacoes: {len(sync_high_stress)}")
    print(f"    Sinc. media: {sync_high_stress.mean():.3f}")
    
    print(f"\n  Periodo de BAIXO estresse (Q1):")
    print(f"    Observacoes: {len(sync_low_stress)}")
    print(f"    Sinc. media: {sync_low_stress.mean():.3f}")
    
    t_stat, p_value = stats.ttest_ind(sync_high_stress.dropna(), 
                                       sync_low_stress.dropna())
    
    print(f"\n  Teste t para diferenca de medias:")
    print(f"    t-statistic: {t_stat:.3f}")
    print(f"    p-value: {p_value:.4f}")
    
    if p_value < 0.05:
        print(f"    -> Diferenca estatisticamente significante")
    else:
        print(f"    -> Diferenca NAO significante")
    
    # Visualizar - figura menor
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    ax1 = axes[0, 0]
    ax1.plot(sync_aligned.index, sync_aligned, label='Sincronizacao', linewidth=1.5)
    ax1.fill_between(sync_aligned.index, 0, 1, where=high_stress, 
                     alpha=0.2, color='red', label='Alto estresse')
    ax1.set_xlabel('Data')
    ax1.set_ylabel('Indice de Sincronizacao')
    ax1.set_title('Evolucao Temporal da Sincronizacao')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2 = axes[0, 1]
    data_to_plot = [sync_low_stress.dropna(), sync_high_stress.dropna()]
    bp = ax2.boxplot(data_to_plot, labels=['Baixo Estresse', 'Alto Estresse'],
                      patch_artist=True)
    bp['boxes'][0].set_facecolor('lightblue')
    bp['boxes'][1].set_facecolor('lightcoral')
    ax2.set_ylabel('Sincronizacao')
    ax2.set_title('Distribuicao por Nivel de Estresse')
    ax2.grid(True, alpha=0.3, axis='y')
    
    ax3 = axes[1, 0]
    ax3.scatter(stress_aligned, sync_aligned, alpha=0.5, s=20)
    ax3.set_xlabel('Indice de Estresse')
    ax3.set_ylabel('Sincronizacao')
    ax3.set_title('Relacao: Estresse x Sincronizacao')
    
    _aligned = pd.concat([stress_aligned, sync_aligned], axis=1).dropna()
    z = np.polyfit(_aligned.iloc[:, 0], _aligned.iloc[:, 1], 1)
    p = np.poly1d(z)
    ax3.plot(_aligned.iloc[:, 0].sort_values(), 
             p(_aligned.iloc[:, 0].sort_values()), 
             "r--", alpha=0.8, linewidth=2)
    ax3.grid(True, alpha=0.3)
    
    ax4 = axes[1, 1]
    ax4.hist(sync_low_stress.dropna(), bins=20, alpha=0.5, 
             label='Baixo Estresse', color='blue', density=True)
    ax4.hist(sync_high_stress.dropna(), bins=20, alpha=0.5, 
             label='Alto Estresse', color='red', density=True)
    ax4.set_xlabel('Sincronizacao')
    ax4.set_ylabel('Densidade')
    ax4.set_title('Distribuicoes Comparadas')
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('figures/synchronization_analysis.png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    print(f"\n  [OK] Grafico salvo: figures/synchronization_analysis.png")
    
    return {
        'high_stress': sync_high_stress,
        'low_stress': sync_low_stress,
        't_stat': t_stat,
        'p_value': p_value
    }

def event_study_defensive():
    """Event study de concentracao defensiva"""
    print("\n[3/4] Event Study: Concentracao Defensiva...")
    
    defensive = pd.read_csv('data/processed/defensive_concentration.csv', 
                           index_col=0, parse_dates=True)
    
    stress = pd.read_csv('data/processed/stress_index.csv', 
                        index_col=0, parse_dates=True)
    
    stress_threshold = stress['STRESS_INDEX'].mean() + 2 * stress['STRESS_INDEX'].std()
    
    events = []
    stress_values = stress['STRESS_INDEX']
    
    for i in range(20, len(stress_values) - 20):
        if stress_values.iloc[i] > stress_threshold:
            window = stress_values.iloc[i-20:i+20]
            if stress_values.iloc[i] == window.max():
                events.append(stress_values.index[i])
    
    print(f"  Eventos de estresse identificados: {len(events)}")
    for event in events:
        event_stress = stress.loc[event, 'STRESS_INDEX']
        print(f"    -> {event.date()}: Stress = {event_stress:.2f}")
    
    if len(events) == 0:
        print("  [AVISO] Nenhum evento identificado")
        return None
    
    window_pre = 126
    window_post = 126
    
    changes_pre = []
    changes_post = []
    
    for event_date in events:
        try:
            event_idx = defensive.index.get_loc(event_date, method='nearest')
            
            if event_idx >= window_pre and event_idx + window_post < len(defensive):
                value_pre_start = defensive.iloc[event_idx - window_pre]['DEFENSIVE_RATIO']
                value_pre_end = defensive.iloc[event_idx - 1]['DEFENSIVE_RATIO']
                value_post_start = defensive.iloc[event_idx + 1]['DEFENSIVE_RATIO']
                value_post_end = defensive.iloc[event_idx + window_post]['DEFENSIVE_RATIO']
                
                change_pre = value_pre_end - value_pre_start
                change_post = value_post_end - value_post_start
                
                changes_pre.append(change_pre)
                changes_post.append(change_post)
        except:
            continue
    
    if len(changes_pre) > 0:
        mean_pre = np.mean(changes_pre)
        mean_post = np.mean(changes_post)
        
        print(f"\n  Mudanca media no Ratio Defensivo:")
        print(f"    6 meses ANTES do evento: {mean_pre:+.2f} pontos")
        print(f"    6 meses DEPOIS do evento: {mean_post:+.2f} pontos")
        
        t_stat, p_value = stats.ttest_1samp(changes_pre, 0)
        
        print(f"\n  Teste t para mudanca pre-evento:")
        print(f"    t-statistic: {t_stat:.3f}")
        print(f"    p-value: {p_value:.4f}")
        
        if p_value < 0.05 and mean_pre > 0:
            print(f"    -> Aumento SIGNIFICATIVO antes de eventos")
        else:
            print(f"    -> Mudanca NAO significante")
        
        return {
            'events': events,
            'mean_pre': mean_pre,
            'mean_post': mean_post
        }
    else:
        print("  [ERRO] Dados insuficientes")
        return None

def generate_comprehensive_report():
    """Gera relatorio visual consolidado"""
    print("\n[4/4] Gerando relatorio visual consolidado...")
    
    try:
        returns = pd.read_csv('data/processed/etf_returns.csv', 
                              index_col=0, parse_dates=True)
        stress = pd.read_csv('data/processed/stress_index.csv', 
                            index_col=0, parse_dates=True)
        sync = pd.read_csv('data/processed/synchronization_index.csv', 
                          index_col=0, parse_dates=True)
        defensive = pd.read_csv('data/processed/defensive_concentration.csv', 
                               index_col=0, parse_dates=True)
        exposure = pd.read_csv('data/processed/exposure_proxy.csv', 
                              index_col=0, parse_dates=True)
        
        fig = plt.figure(figsize=(14, 10))
        gs = fig.add_gridspec(4, 2, hspace=0.3, wspace=0.3)
        
        ax1 = fig.add_subplot(gs[0, :])
        china_etfs = ['FXI', 'MCHI', 'KWEB']
        available = [etf for etf in china_etfs if etf in returns.columns]
        
        for etf in available:
            cumulative = (1 + returns[etf]).cumprod()
            ax1.plot(cumulative.index, cumulative, label=etf, linewidth=1.5)
        
        ax1.set_ylabel('Retorno Acumulado (Base 1)')
        ax1.set_title('Retornos Cumulativos: ETFs China', fontsize=11, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.plot(stress.index, stress['STRESS_INDEX'], color='red', linewidth=1.2)
        ax2.axhline(y=0, color='k', linestyle='--', linewidth=0.5)
        ax2.axhline(y=2, color='r', linestyle='--', linewidth=0.5, alpha=0.3)
        ax2.fill_between(stress.index, 0, stress['STRESS_INDEX'], 
                         where=(stress['STRESS_INDEX'] > 2), 
                         alpha=0.2, color='red')
        ax2.set_ylabel('Z-score')
        ax2.set_title('Indice de Estresse', fontsize=10, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        ax3 = fig.add_subplot(gs[1, 1])
        ax3.plot(sync.index, sync['SYNC_INDEX'], color='blue', linewidth=1.2)
        ax3.set_ylabel('Correlacao')
        ax3.set_title('Sincronizacao Institucional', fontsize=10, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        
        ax4 = fig.add_subplot(gs[2, 0])
        ax4.plot(exposure.index, exposure['EXPOSURE_RATIO'], color='green', linewidth=1.2)
        ax4.set_ylabel('Ratio (Base 100)')
        ax4.set_title('Exposicao (FXI/SPY)', fontsize=10, fontweight='bold')
        ax4.grid(True, alpha=0.3)
        
        ax5 = fig.add_subplot(gs[2, 1])
        ax5.plot(defensive.index, defensive['DEFENSIVE_RATIO'], 
                 color='orange', linewidth=1.2)
        ax5.set_ylabel('Ratio (Base 100)')
        ax5.set_title('Defensivo (GLD/FXI)', fontsize=10, fontweight='bold')
        ax5.grid(True, alpha=0.3)
        
        ax6 = fig.add_subplot(gs[3, :])
        ax6.axis('off')
        
        summary_text = f"""
        FRAMEWORK DE PREPARACAO ASSIMETRICA - RESUMO
        
        Periodo: {stress.index[0].strftime('%Y-%m')} ate {stress.index[-1].strftime('%Y-%m')}
        
        ESTRESSE: Media={stress['STRESS_INDEX'].mean():.2f} | Max={stress['STRESS_INDEX'].max():.2f}
        SINCRONIZACAO: Media={sync['SYNC_INDEX'].mean():.3f} | Range=[{sync['SYNC_INDEX'].min():.3f}, {sync['SYNC_INDEX'].max():.3f}]
        EXPOSICAO: Inicio={exposure['EXPOSURE_RATIO'].iloc[0]:.1f} | Fim={exposure['EXPOSURE_RATIO'].iloc[-1]:.1f}
        """
        
        ax6.text(0.1, 0.5, summary_text, fontsize=8, verticalalignment='center',
                 fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        
        plt.suptitle('Framework Preparacao Assimetrica: Painel Consolidado', 
                     fontsize=12, fontweight='bold', y=0.995)
        
        plt.savefig('figures/comprehensive_report.png', dpi=100, bbox_inches='tight')
        plt.close(fig)
        print(f"  [OK] Relatorio consolidado salvo")
        
    except Exception as e:
        print(f"  [ERRO] Erro ao gerar relatorio: {str(e)}")

def generate_summary():
    """Gera resumo"""
    print("\n" + "="*60)
    print("RESUMO DA ANALISE DE SINCRONIZACAO")
    print("="*60)
    
    outputs = {
        'figures/synchronization_analysis.png': 'Analise de sincronizacao',
        'figures/comprehensive_report.png': 'Relatorio consolidado'
    }
    
    for file, description in outputs.items():
        if os.path.exists(file):
            print(f"[OK] {description:35s} -> {file}")
        else:
            print(f"[--] {description:35s} -> Nao gerado")
    
    print("\n[OK] Analise de sincronizacao concluida!")
    print("[OK] Todos os componentes foram executados")
    print("="*60)

def main():
    """Funcao principal"""
    print("="*60)
    print("FRAMEWORK: PREPARACAO ASSIMETRICA")
    print("Script 03: Analise de Sincronizacao")
    print("="*60)
    
    required_files = [
        'data/processed/etf_returns.csv',
        'data/processed/stress_index.csv'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"\n[ERRO] {file} nao encontrado!")
            return
    
    os.makedirs('figures', exist_ok=True)
    plt.close('all')
    
    sync_df = calculate_rolling_correlation()
    
    if sync_df is not None:
        compare_periods()
        event_study_defensive()
        generate_comprehensive_report()
    
    plt.close('all')
    generate_summary()

if __name__ == "__main__":
    main()
