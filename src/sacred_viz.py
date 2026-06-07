"""
============================================================
PROJECT ALPHA: LAUNCH ECONOMICS
Sacred Visualization Module
============================================================
Custom visualization utilities implementing the Sacred Neo-Byzantine
aesthetic system for aerospace data science analytics.

Author: [Your Name]
Date: 2026-06-06
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, Wedge, FancyBboxPatch, Ellipse, Polygon
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
from typing import Optional, Tuple, List, Dict
import warnings
warnings.filterwarnings('ignore')


class SacredPalette:
    """
    The Sacred Neo-Byzantine color system.

    A chromatic ontology mapping colors to symbolic meanings
    drawn from sacred geometry, organic nature, and DMT visionary states.
    """

    COLORS = {
        'deep_void': '#0A0A1A',
        'nebula_purple': '#4A0E4E',
        'sacred_gold': '#D4AF37',
        'mystic_teal': '#0D7377',
        'organic_emerald': '#1B5E20',
        'dmt_coral': '#FF6B6B',
        'ethereal_blue': '#4FC3F7',
        'amber_resin': '#FF8F00',
        'sacred_crimson': '#B71C1C',
        'mushroom_ivory': '#FFF8E1',
        'forest_deep': '#1B4332',
        'lotus_pink': '#F8BBD0',
        'mandala_orange': '#FF5722',
        'crystal_cyan': '#00BCD4',
        'obsidian': '#1C1C1C',
    }

    @classmethod
    def get(cls, name: str) -> str:
        """Retrieve color by sacred name."""
        return cls.COLORS.get(name, cls.COLORS['deep_void'])

    @classmethod
    def get_cmap(cls, name: str) -> LinearSegmentedColormap:
        """Retrieve registered colormap."""
        import matplotlib
        return matplotlib.colormaps.get_cmap(name)

    @classmethod
    def setup_figure(cls, fig: Optional[plt.Figure] = None) -> plt.Figure:
        """Configure figure with sacred defaults."""
        if fig is None:
            fig = plt.gcf()
        fig.patch.set_facecolor(cls.COLORS['deep_void'])
        return fig

    @classmethod
    def setup_axes(cls, ax: Optional[plt.Axes] = None) -> plt.Axes:
        """Configure axes with sacred defaults."""
        if ax is None:
            ax = plt.gca()
        ax.set_facecolor(cls.COLORS['deep_void'])
        ax.tick_params(colors=cls.COLORS['mushroom_ivory'])
        for spine in ax.spines.values():
            spine.set_color(cls.COLORS['sacred_gold'])
            spine.set_linewidth(0.8)
        ax.xaxis.label.set_color(cls.COLORS['mushroom_ivory'])
        ax.yaxis.label.set_color(cls.COLORS['mushroom_ivory'])
        ax.title.set_color(cls.COLORS['sacred_gold'])
        return ax


class SacredPlotter:
    """
    High-level plotting interface for sacred aesthetic visualizations.

    Implements geometric primitives inspired by:
    - Sacred geometry (mandala, flower of life, golden spiral)
    - Organic forms (tree branches, leaf venation, cellular structures)
    - DMT visionary art (chromatic gradients, fractal recursion, luminous entities)
    - Byzantine manuscript illumination (gold leaf, crimson borders, illuminated initials)
    """

    def __init__(self):
        self.palette = SacredPalette()
        self._register_colormaps()
        self._setup_global_style()

    def _register_colormaps(self):
        """Register custom colormaps with matplotlib."""
        import matplotlib

        cmaps = {
            'sacred_gradient': [
                self.palette.COLORS['deep_void'],
                self.palette.COLORS['nebula_purple'],
                self.palette.COLORS['sacred_gold'],
                self.palette.COLORS['mystic_teal'],
                self.palette.COLORS['organic_emerald']
            ],
            'dmt_vision': [
                '#1A0033', '#4A0E4E', '#D4AF37', '#FF6B6B', '#00BCD4', '#FFF8E1'
            ],
            'organic_nature': [
                '#0A1F0A', '#1B5E20', '#2E7D32', '#FF8F00', '#FFF8E1'
            ],
            'byzantine_sacred': [
                '#4A0000', '#B71C1C', '#D4AF37', '#1A237E', '#0A0A1A'
            ],
        }

        for name, colors in cmaps.items():
            cmap = LinearSegmentedColormap.from_list(name, colors)
            try:
                matplotlib.colormaps.register(cmap=cmap)
            except ValueError:
                pass  # Already registered

    def _setup_global_style(self):
        """Configure matplotlib global style parameters."""
        plt.rcParams['figure.facecolor'] = self.palette.COLORS['deep_void']
        plt.rcParams['axes.facecolor'] = self.palette.COLORS['deep_void']
        plt.rcParams['text.color'] = self.palette.COLORS['mushroom_ivory']
        plt.rcParams['axes.labelcolor'] = self.palette.COLORS['mushroom_ivory']
        plt.rcParams['xtick.color'] = self.palette.COLORS['mushroom_ivory']
        plt.rcParams['ytick.color'] = self.palette.COLORS['mushroom_ivory']
        plt.rcParams['axes.edgecolor'] = self.palette.COLORS['sacred_gold']
        plt.rcParams['axes.grid'] = True
        plt.rcParams['grid.color'] = 'rgba(212, 175, 55, 0.15)'
        plt.rcParams['grid.linewidth'] = 0.5
        plt.rcParams['font.family'] = 'serif'
        plt.rcParams['font.serif'] = ['Georgia', 'Times New Roman', 'DejaVu Serif']

    def create_mandala(self, df: pd.DataFrame, 
                     title: str = "Sacred Mandala",
                     figsize: Tuple[int, int] = (20, 20)) -> plt.Figure:
        """
        Create a 3x3 mandala dashboard with sacred aesthetic.

        Parameters:
        -----------
        df : pd.DataFrame
            Processed launch data
        title : str
            Mandala title
        figsize : tuple
            Figure dimensions

        Returns:
        --------
        plt.Figure
            Configured figure object
        """
        fig = plt.figure(figsize=figsize, facecolor=self.palette.COLORS['deep_void'])
        gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.35)

        # Title
        fig.suptitle(f'⟁ {title} ⟁', 
                    fontsize=18, fontweight='bold', 
                    color=self.palette.COLORS['sacred_gold'], y=0.98)

        # Panel 1: Temporal evolution
        ax1 = fig.add_subplot(gs[0, 0])
        self._plot_temporal_cadence(ax1, df)

        # Panel 2: Cost descent
        ax2 = fig.add_subplot(gs[0, 1])
        self._plot_cost_descent(ax2, df)

        # Panel 3: Orbital destiny
        ax3 = fig.add_subplot(gs[0, 2])
        self._plot_orbital_destiny(ax3, df)

        # Panel 4: Sacred sites
        ax4 = fig.add_subplot(gs[1, 0])
        self._plot_sacred_sites(ax4, df)

        # Panel 5: Reuse alchemy
        ax5 = fig.add_subplot(gs[1, 1])
        self._plot_reuse_alchemy(ax5, df)

        # Panel 6: Payload harmonics
        ax6 = fig.add_subplot(gs[1, 2])
        self._plot_payload_harmonics(ax6, df)

        # Panel 7: Learning curve
        ax7 = fig.add_subplot(gs[2, 0])
        self._plot_learning_curve(ax7, df)

        # Panel 8: Block evolution
        ax8 = fig.add_subplot(gs[2, 1])
        self._plot_block_evolution(ax8, df)

        # Panel 9: Sacred metrics
        ax9 = fig.add_subplot(gs[2, 2])
        self._plot_sacred_metrics(ax9, df)

        return fig

    def _plot_temporal_cadence(self, ax: plt.Axes, df: pd.DataFrame):
        """Plot temporal launch cadence with dual-axis success tracking."""
        self.palette.setup_axes(ax)

        yearly = df.groupby('Year').agg({
            'FlightNumber': 'count',
            'Success': 'mean',
        }).reset_index()
        yearly.columns = ['Year', 'Launches', 'SuccessRate']

        ax_twin = ax.twinx()
        ax_twin.set_facecolor(self.palette.COLORS['deep_void'])
        ax_twin.tick_params(axis='y', labelcolor=self.palette.COLORS['crystal_cyan'])
        ax_twin.spines['right'].set_color(self.palette.COLORS['sacred_gold'])

        bars = ax.bar(yearly['Year'], yearly['Launches'], 
                     color=self.palette.COLORS['amber_resin'], alpha=0.7,
                     width=0.6, edgecolor=self.palette.COLORS['sacred_gold'], linewidth=1)

        ax_twin.plot(yearly['Year'], yearly['SuccessRate']*100, 
                    color=self.palette.COLORS['crystal_cyan'], linewidth=3,
                    marker='o', markersize=8, markerfacecolor=self.palette.COLORS['ethereal_blue'])
        ax_twin.fill_between(yearly['Year'], yearly['SuccessRate']*100, 
                            alpha=0.2, color=self.palette.COLORS['crystal_cyan'])

        ax.set_xlabel('Year', fontsize=10)
        ax.set_ylabel('Launches', fontsize=10, color=self.palette.COLORS['amber_resin'])
        ax_twin.set_ylabel('Success Rate (%)', fontsize=10, color=self.palette.COLORS['crystal_cyan'])
        ax.set_title('◈ Temporal Cadence & Success Evolution ◈', 
                    fontsize=11, color=self.palette.COLORS['sacred_gold'], fontweight='bold')

    def _plot_cost_descent(self, ax: plt.Axes, df: pd.DataFrame):
        """Plot cost per kg descent curve over time."""
        self.palette.setup_axes(ax)

        scatter = ax.scatter(df['DaysSinceFirst'], df['CostPerKg'],
                           c=df['Success'], cmap='dmt_vision', s=80, alpha=0.8,
                           edgecolors=self.palette.COLORS['sacred_gold'], linewidth=0.5)

        z = np.polyfit(df['DaysSinceFirst'], df['CostPerKg'], 2)
        p = np.poly1d(z)
        x_line = np.linspace(df['DaysSinceFirst'].min(), df['DaysSinceFirst'].max(), 100)
        ax.plot(x_line, p(x_line), color=self.palette.COLORS['dmt_coral'], 
               linewidth=2, linestyle='--', alpha=0.8)

        ax.set_xlabel('Days Since First Launch', fontsize=10)
        ax.set_ylabel('Cost Per Kg (USD)', fontsize=10)
        ax.set_title('◈ The Descent of Cost: Orbital Economics ◈', 
                    fontsize=11, color=self.palette.COLORS['sacred_gold'], fontweight='bold')
        ax.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))

    def _plot_orbital_destiny(self, ax: plt.Axes, df: pd.DataFrame):
        """Plot success rates by orbital destination."""
        self.palette.setup_axes(ax)

        orbit_success = df.groupby('Orbit')['Success'].agg(['mean', 'count']).reset_index()
        orbit_success = orbit_success.sort_values('mean', ascending=True)

        colors = [self.palette.COLORS['organic_emerald'] if x > 0.8 
                 else self.palette.COLORS['amber_resin'] if x > 0.6 
                 else self.palette.COLORS['dmt_coral'] 
                 for x in orbit_success['mean']]

        bars = ax.barh(orbit_success['Orbit'], orbit_success['mean']*100,
                      color=colors, edgecolor=self.palette.COLORS['sacred_gold'], 
                      linewidth=1, height=0.6)

        for bar, count in zip(bars, orbit_success['count']):
            ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                   f'n={count}', va='center', fontsize=8, 
                   color=self.palette.COLORS['mushroom_ivory'])

        ax.set_xlabel('Success Rate (%)', fontsize=10)
        ax.set_title('◈ Orbital Destiny: Success by Trajectory ◈', 
                    fontsize=11, color=self.palette.COLORS['sacred_gold'], fontweight='bold')
        ax.set_xlim(0, 105)

    def _plot_sacred_sites(self, ax: plt.Axes, df: pd.DataFrame):
        """Create sacred flower/petal chart for launch sites."""
        ax.set_facecolor(self.palette.COLORS['deep_void'])
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_aspect('equal')
        ax.axis('off')

        site_stats = df.groupby('LaunchSite').agg({
            'FlightNumber': 'count',
            'Success': 'mean',
        }).reset_index()

        sites = site_stats['LaunchSite'].values
        angles = np.linspace(0, 2*np.pi, len(sites), endpoint=False)
        values = site_stats['FlightNumber'].values
        values_norm = values / values.max() * 0.8

        site_colors = [self.palette.COLORS['sacred_crimson'], 
                      self.palette.COLORS['mystic_teal'], 
                      self.palette.COLORS['amber_resin']]

        for angle, val, site, color in zip(angles, values_norm, sites, site_colors):
            theta = np.linspace(angle - 0.3, angle + 0.3, 50)
            r = np.linspace(0, val, 50)
            theta_grid, r_grid = np.meshgrid(theta, r)
            x = r_grid * np.cos(theta_grid)
            y = r_grid * np.sin(theta_grid)
            ax.fill(x.flatten(), y.flatten(), color=color, alpha=0.6, 
                   edgecolor=self.palette.COLORS['sacred_gold'])

            label_r = val + 0.15
            ax.text(label_r * np.cos(angle), label_r * np.sin(angle),
                   f'{site}\n({int(values[list(angles).index(angle)])})',
                   ha='center', va='center', fontsize=9, 
                   color=self.palette.COLORS['mushroom_ivory'], fontweight='bold')

        center = Circle((0, 0), 0.1, color=self.palette.COLORS['sacred_gold'], alpha=0.9)
        ax.add_patch(center)
        ax.text(0, 0, 'SPACEX', ha='center', va='center', fontsize=8,
               color=self.palette.COLORS['deep_void'], fontweight='bold')

        ax.set_title('◈ Sacred Launch Sites: The Three Temples ◈', 
                    fontsize=11, color=self.palette.COLORS['sacred_gold'], fontweight='bold')

    def _plot_reuse_alchemy(self, ax: plt.Axes, df: pd.DataFrame):
        """Plot the alchemy of reuse: cost transformation."""
        self.palette.setup_axes(ax)

        reused_df = df[df['Reused'] == True]
        new_df = df[df['Reused'] == False]

        ax.scatter(new_df['PayloadMass'], new_df['CostPerKg'],
                  c=self.palette.COLORS['dmt_coral'], s=100, alpha=0.7,
                  label='New Booster', edgecolors=self.palette.COLORS['sacred_gold'],
                  linewidth=1, marker='s')
        ax.scatter(reused_df['PayloadMass'], reused_df['CostPerKg'],
                  c=self.palette.COLORS['organic_emerald'], s=100, alpha=0.7,
                  label='Reused Booster', edgecolors=self.palette.COLORS['sacred_gold'],
                  linewidth=1, marker='o')

        ax.set_xlabel('Payload Mass (kg)', fontsize=10)
        ax.set_ylabel('Cost Per Kg (USD)', fontsize=10)
        ax.set_title('◈ The Alchemy of Reuse: Cost Transformation ◈', 
                    fontsize=11, color=self.palette.COLORS['sacred_gold'], fontweight='bold')
        ax.legend(facecolor=self.palette.COLORS['deep_void'],
                 edgecolor=self.palette.COLORS['sacred_gold'],
                 labelcolor=self.palette.COLORS['mushroom_ivory'])
        ax.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))

    def _plot_payload_harmonics(self, ax: plt.Axes, df: pd.DataFrame):
        """Plot payload distribution by orbital plane."""
        self.palette.setup_axes(ax)

        orbits = df['Orbit'].unique()
        data_groups = [df[df['Orbit'] == o]['PayloadMass'].values for o in orbits]

        parts = ax.violinplot(data_groups, positions=range(len(orbits)),
                             showmeans=True, showmedians=True)

        colors_list = [self.palette.COLORS['nebula_purple'], 
                      self.palette.COLORS['mystic_teal'],
                      self.palette.COLORS['amber_resin'],
                      self.palette.COLORS['organic_emerald'],
                      self.palette.COLORS['dmt_coral'],
                      self.palette.COLORS['crystal_cyan']]

        for i, pc in enumerate(parts['bodies']):
            pc.set_facecolor(colors_list[i % len(colors_list)])
            pc.set_alpha(0.6)
            pc.set_edgecolor(self.palette.COLORS['sacred_gold'])

        for partname in ('cbars', 'cmins', 'cmaxes', 'cmeans', 'cmedians'):
            if partname in parts:
                parts[partname].set_color(self.palette.COLORS['sacred_gold'])
                parts[partname].set_linewidth(1.5)

        ax.set_xticks(range(len(orbits)))
        ax.set_xticklabels(orbits, rotation=45, ha='right')
        ax.set_ylabel('Payload Mass (kg)', fontsize=10)
        ax.set_title('◈ Payload Harmonics by Orbital Plane ◈', 
                    fontsize=11, color=self.palette.COLORS['sacred_gold'], fontweight='bold')

    def _plot_learning_curve(self, ax: plt.Axes, df: pd.DataFrame):
        """Plot cumulative success rate learning curve."""
        self.palette.setup_axes(ax)

        ax.plot(df['FlightNumber'], df['RollingSuccessRate']*100,
               color=self.palette.COLORS['crystal_cyan'], linewidth=2.5)
        ax.fill_between(df['FlightNumber'], df['RollingSuccessRate']*100,
                       alpha=0.3, color=self.palette.COLORS['crystal_cyan'])

        first_success = df[df['Success'] == 1]['FlightNumber'].iloc[0] if any(df['Success'] == 1) else 0
        if first_success > 0:
            ax.axvline(x=first_success, color=self.palette.COLORS['sacred_gold'],
                      linestyle='--', alpha=0.7, linewidth=2)
            ax.text(first_success+2, 50, 'First Landing\nSuccess', fontsize=8,
                   color=self.palette.COLORS['sacred_gold'],
                   bbox=dict(boxstyle='round,pad=0.3', 
                            facecolor=self.palette.COLORS['nebula_purple'], alpha=0.7))

        ax.set_xlabel('Flight Number', fontsize=10)
        ax.set_ylabel('Cumulative Success Rate (%)', fontsize=10)
        ax.set_title('◈ The Learning Curve: Path to Mastery ◈', 
                    fontsize=11, color=self.palette.COLORS['sacred_gold'], fontweight='bold')
        ax.set_ylim(0, 105)

    def _plot_block_evolution(self, ax: plt.Axes, df: pd.DataFrame):
        """Plot generational block evolution with sacred circles."""
        self.palette.setup_axes(ax)

        block_stats = df.groupby('Block').agg({
            'Success': 'mean',
            'FlightNumber': 'count',
            'CostPerKg': 'mean'
        }).reset_index()

        dmt_cmap = self.palette.get_cmap('dmt_vision')

        for i, row in block_stats.iterrows():
            x = row['Block']
            y = row['Success'] * 100
            size = row['FlightNumber'] * 30

            cost_range = block_stats['CostPerKg'].max() - block_stats['CostPerKg'].min()
            if cost_range > 0:
                color_intensity = 1 - (row['CostPerKg'] - block_stats['CostPerKg'].min()) / cost_range
            else:
                color_intensity = 0.5

            circle = Circle((x, y), size/200, color=dmt_cmap(color_intensity),
                          alpha=0.7, edgecolor=self.palette.COLORS['sacred_gold'], linewidth=2)
            ax.add_patch(circle)
            ax.text(x, y, f"B{int(row['Block'])}\n{int(row['FlightNumber'])} flights",
                   ha='center', va='center', fontsize=8,
                   color=self.palette.COLORS['mushroom_ivory'], fontweight='bold')

        ax.set_xlim(0.5, 5.5)
        ax.set_ylim(0, 105)
        ax.set_xlabel('Block Version', fontsize=10)
        ax.set_ylabel('Success Rate (%)', fontsize=10)
        ax.set_title('◈ Generational Evolution: Block Sacred Circles ◈', 
                    fontsize=11, color=self.palette.COLORS['sacred_gold'], fontweight='bold')
        ax.set_xticks([1, 2, 3, 4, 5])

    def _plot_sacred_metrics(self, ax: plt.Axes, df: pd.DataFrame):
        """Display key metrics in sacred illuminated boxes."""
        ax.set_facecolor(self.palette.COLORS['deep_void'])
        ax.axis('off')

        metrics = [
            ('⟁ Total Launches', f"{len(df)}", self.palette.COLORS['sacred_gold']),
            ('◈ Success Rate', f"{df['Success'].mean()*100:.1f}%", self.palette.COLORS['crystal_cyan']),
            ('✦ Reused Boosters', f"{df['Reused'].sum()}", self.palette.COLORS['organic_emerald']),
            ('◉ Avg Cost/kg', f"${df['CostPerKg'].mean():,.0f}", self.palette.COLORS['amber_resin']),
            ('⚛ Savings vs Competitor', f"${(df['CompetitorCost'] - df['EstimatedCost']).mean():.0f}M", 
             self.palette.COLORS['dmt_coral']),
            ('✧ Starlink Era', f"{len(df[df['PayloadMass'] > 10000])} launches", 
             self.palette.COLORS['lotus_pink']),
        ]

        for i, (label, value, color) in enumerate(metrics):
            y_pos = 0.85 - i * 0.15
            box = FancyBboxPatch((0.05, y_pos-0.05), 0.9, 0.12,
                               boxstyle="round,pad=0.02,rounding_size=0.02",
                               facecolor=self.palette.COLORS['nebula_purple'],
                               edgecolor=color, alpha=0.3, linewidth=2,
                               transform=ax.transAxes)
            ax.add_patch(box)
            ax.text(0.5, y_pos+0.01, label, ha='center', va='center',
                   fontsize=10, color=color, fontweight='bold', transform=ax.transAxes)
            ax.text(0.5, y_pos-0.03, value, ha='center', va='center',
                   fontsize=14, color=self.palette.COLORS['mushroom_ivory'], 
                   fontweight='bold', transform=ax.transAxes)

        ax.set_title('◈ The Sacred Metrics ◈', 
                    fontsize=11, color=self.palette.COLORS['sacred_gold'], 
                    fontweight='bold', pad=20)

    def create_byzantine_rose(self, df: pd.DataFrame,
                             figsize: Tuple[int, int] = (14, 14)) -> plt.Figure:
        """
        Create a Byzantine rose chart for seasonal launch patterns.

        Parameters:
        -----------
        df : pd.DataFrame
            Processed launch data
        figsize : tuple
            Figure dimensions

        Returns:
        --------
        plt.Figure
            Rose chart figure
        """
        fig, ax = plt.subplots(figsize=figsize, facecolor=self.palette.COLORS['deep_void'])
        ax.set_facecolor(self.palette.COLORS['deep_void'])
        ax.set_xlim(-12, 12)
        ax.set_ylim(-12, 12)
        ax.set_aspect('equal')
        ax.axis('off')

        monthly = df.groupby('Month').agg({'FlightNumber': 'count', 'Success': 'mean'}).reset_index()
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        angles = np.linspace(0, 2*np.pi, 12, endpoint=False)
        values = monthly['FlightNumber'].values
        success_rates = monthly['Success'].values * 100

        for i in range(12):
            if success_rates[i] >= 90:
                color = self.palette.COLORS['organic_emerald']
            elif success_rates[i] >= 70:
                color = self.palette.COLORS['amber_resin']
            else:
                color = self.palette.COLORS['dmt_coral']

            theta1 = np.degrees(angles[i]) - 12
            theta2 = np.degrees(angles[i]) + 12
            wedge = Wedge((0, 0), values[i], theta1, theta2,
                         facecolor=color, alpha=0.6,
                         edgecolor=self.palette.COLORS['sacred_gold'], linewidth=1.5)
            ax.add_patch(wedge)

            label_r = values[i] + 1.5
            ax.text(label_r * np.cos(angles[i]), label_r * np.sin(angles[i]),
                   f'{months[i]}\n({values[i]})', ha='center', va='center',
                   fontsize=9, color=self.palette.COLORS['mushroom_ivory'], fontweight='bold')

        circle_ref = Circle((0, 0), 5, fill=False, 
                           color=self.palette.COLORS['sacred_gold'],
                           linestyle='--', alpha=0.5, linewidth=1)
        ax.add_patch(circle_ref)

        ax.set_title('⟁ The Byzantine Rose: Seasonal Launch Cadence ⟁',
                    fontsize=14, color=self.palette.COLORS['sacred_gold'], 
                    fontweight='bold', pad=20)

        return fig

    def create_sacred_spiral(self, df: pd.DataFrame,
                            figsize: Tuple[int, int] = (10, 10)) -> plt.Figure:
        """
        Create a sacred spiral visualization of cumulative savings.

        Parameters:
        -----------
        df : pd.DataFrame
            Processed launch data
        figsize : tuple
            Figure dimensions

        Returns:
        --------
        plt.Figure
            Spiral figure
        """
        fig, ax = plt.subplots(figsize=figsize, facecolor=self.palette.COLORS['deep_void'])
        ax.set_facecolor(self.palette.COLORS['deep_void'])
        ax.set_xlim(-14, 14)
        ax.set_ylim(-14, 14)
        ax.set_aspect('equal')
        ax.axis('off')

        df_sorted = df.sort_values('Date')
        df_sorted['CumulativeSavings'] = (df_sorted['CompetitorCost'] - 
                                          df_sorted['EstimatedCost']).cumsum()

        n_points = len(df_sorted)
        theta = np.linspace(0, 4*np.pi, n_points)
        r = np.linspace(1, 10, n_points)

        x_spiral = r * np.cos(theta)
        y_spiral = r * np.sin(theta)

        dmt_cmap = self.palette.get_cmap('dmt_vision')
        colors = dmt_cmap(np.linspace(0, 1, n_points))

        for i in range(n_points - 1):
            ax.plot([x_spiral[i], x_spiral[i+1]], 
                   [y_spiral[i], y_spiral[i+1]],
                   color=colors[i], linewidth=3, alpha=0.8)

        milestones = [0, n_points//3, 2*n_points//3, n_points-1]
        for m in milestones:
            ax.scatter(x_spiral[m], y_spiral[m], s=200, c=[colors[m]],
                      edgecolors=self.palette.COLORS['sacred_gold'], 
                      linewidth=2, zorder=10)
            ax.text(x_spiral[m]*1.15, y_spiral[m]*1.15,
                   f'${df_sorted.iloc[m]["CumulativeSavings"]:.0f}M\nsaved',
                   fontsize=8, color=self.palette.COLORS['mushroom_ivory'], 
                   ha='center',
                   bbox=dict(boxstyle='round,pad=0.3',
                            facecolor=self.palette.COLORS['nebula_purple'],
                            edgecolor=self.palette.COLORS['sacred_gold'], alpha=0.8))

        center_circle = Circle((0, 0), 0.5, 
                              color=self.palette.COLORS['sacred_gold'], alpha=0.9)
        ax.add_patch(center_circle)
        ax.text(0, 0, 
               f'${df_sorted["CumulativeSavings"].iloc[-1]:.0f}M\nTOTAL',
               ha='center', va='center', fontsize=9,
               color=self.palette.COLORS['deep_void'], fontweight='bold')

        ax.set_title('⟁ The Sacred Spiral: Cumulative Economic Liberation ⟁',
                    fontsize=14, color=self.palette.COLORS['sacred_gold'],
                    fontweight='bold', pad=20)

        return fig


if __name__ == '__main__':
    # Example usage
    df = pd.read_csv('data/spacex_raw.csv')

    plotter = SacredPlotter()

    # Create mandala
    fig = plotter.create_mandala(df, title="Launch Economics Overview")
    fig.savefig('dashboard/sacred_mandala_example.png', 
               dpi=150, facecolor='#0A0A1A', bbox_inches='tight')
    print("✅ Sacred Mandala saved!")

    # Create Byzantine Rose
    fig_rose = plotter.create_byzantine_rose(df)
    fig_rose.savefig('dashboard/byzantine_rose_example.png',
                    dpi=150, facecolor='#0A0A1A', bbox_inches='tight')
    print("✅ Byzantine Rose saved!")

    # Create Sacred Spiral
    fig_spiral = plotter.create_sacred_spiral(df)
    fig_spiral.savefig('dashboard/sacred_spiral_example.png',
                      dpi=150, facecolor='#0A0A1A', bbox_inches='tight')
    print("✅ Sacred Spiral saved!")
