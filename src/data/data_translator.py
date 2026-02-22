from src.data.data_loader import DataLoader


class DataTranslator:
    def __init__(self,
                 data_loader: DataLoader
                 ):
        self.corner_passing_orders = data_loader.corner_passing_orders
        self.translate_corner_passing_orders()

        self.laptimes = data_loader.laptimes
        self.translate_laptimes()

        self.odds = data_loader.odds
        self.translate_odds()

        self.race_results = data_loader.race_results
        self.translate_race_results()

    def translate_corner_passing_orders(self):
        col_map = {
            'レースID': 'race_id',

            '1コーナー': 'corner_1',
            '2コーナー': 'corner_2',
            '3コーナー': 'corner_3',
            '4コーナー': 'corner_4'
        }
        self.corner_passing_orders.rename(columns=col_map, inplace=True)

    def translate_laptimes(self):
        col_map = {
            'レースID': 'race_id',

            'ラップタイム1': 'lap_time_1', 'ラップタイム2': 'lap_time_2',
            'ラップタイム3': 'lap_time_3', 'ラップタイム4': 'lap_time_4',
            'ラップタイム5': 'lap_time_5', 'ラップタイム6': 'lap_time_6',
            'ラップタイム7': 'lap_time_7', 'ラップタイム8': 'lap_time_8',
            'ラップタイム9': 'lap_time_9', 'ラップタイム10': 'lap_time_10',
            'ラップタイム11': 'lap_time_11', 'ラップタイム12': 'lap_time_12',
            'ラップタイム13': 'lap_time_13', 'ラップタイム14': 'lap_time_14',
            'ラップタイム15': 'lap_time_15', 'ラップタイム16': 'lap_time_16',
            'ラップタイム17': 'lap_time_17', 'ラップタイム18': 'lap_time_18',

            'ペース1': 'pace_1', 'ペース2': 'pace_2', 'ペース3': 'pace_3',
            'ペース4': 'pace_4', 'ペース5': 'pace_5', 'ペース6': 'pace_6',
            'ペース7': 'pace_7', 'ペース8': 'pace_8', 'ペース9': 'pace_9',
            'ペース10': 'pace_10', 'ペース11': 'pace_11', 'ペース12': 'pace_12',
            'ペース13': 'pace_13', 'ペース14': 'pace_14', 'ペース15': 'pace_15',
            'ペース16': 'pace_16', 'ペース17': 'pace_17', 'ペース18': 'pace_18',

            '前半3ハロン': 'f3f',
            '上がり3ハロン': 'l3f'
        }
        self.laptimes.rename(columns=col_map, inplace=True)

    def translate_odds(self):
        column_map = {
            'レースID': 'race_id',

            '単勝1_馬番': 'win_1_pp', '単勝2_馬番': 'win_2_pp',
            '単勝1_オッズ': 'win_1_odds', '単勝2_オッズ': 'win_2_odds',
            '単勝1_人気': 'win_1_popularity', '単勝2_人気': 'win_2_popularity',

            '複勝1_馬番': 'place_1_pp', '複勝2_馬番': 'place_2_pp', '複勝3_馬番': 'place_3_pp',
            '複勝4_馬番': 'place_4_pp', '複勝5_馬番': 'place_5_pp',
            '複勝1_オッズ': 'place_1_odds', '複勝2_オッズ': 'place_2_odds', '複勝3_オッズ': 'place_3_odds',
            '複勝4_オッズ': 'place_4_odds', '複勝5_オッズ': 'place_5_odds',
            '複勝1_人気': 'place_1_popularity', '複勝2_人気': 'place_2_popularity',
            '複勝3_人気': 'place_3_popularity', '複勝4_人気': 'place_4_popularity', '複勝5_人気': 'place_5_popularity',

            '枠連1_組合せ1': 'bracket_q_1_comb1', '枠連1_組合せ2': 'bracket_q_1_comb2',
            '枠連2_組合せ1': 'bracket_q_2_comb1', '枠連2_組合せ2': 'bracket_q_2_comb2',
            '枠連1_オッズ': 'bracket_q_1_odds', '枠連2_オッズ': 'bracket_q_2_odds',
            '枠連1_人気': 'bracket_q_1_popularity', '枠連2_人気': 'bracket_q_2_popularity',

            '馬連1_組合せ1': 'quinella_1_comb1', '馬連1_組合せ2': 'quinella_1_comb2',
            '馬連2_組合せ1': 'quinella_2_comb1', '馬連2_組合せ2': 'quinella_2_comb2',
            '馬連1_オッズ': 'quinella_1_odds', '馬連2_オッズ': 'quinella_2_odds',
            '馬連1_人気': 'quinella_1_popularity', '馬連2_人気': 'quinella_2_popularity',

            'ワイド1_組合せ1': 'wide_1_comb1', 'ワイド1_組合せ2': 'wide_1_comb2',
            'ワイド2_組合せ1': 'wide_2_comb1', 'ワイド2_組合せ2': 'wide_2_comb2',
            'ワイド3_組合せ1': 'wide_3_comb1', 'ワイド3_組合せ2': 'wide_3_comb2',
            'ワイド4_組合せ1': 'wide_4_comb1', 'ワイド4_組合せ2': 'wide_4_comb2',
            'ワイド5_組合せ1': 'wide_5_comb1', 'ワイド5_組合せ2': 'wide_5_comb2',
            'ワイド6_組合せ1': 'wide_6_comb1', 'ワイド6_組合せ2': 'wide_6_comb2',
            'ワイド7_組合せ1': 'wide_7_comb1', 'ワイド7_組合せ2': 'wide_7_comb2',
            'ワイド1_オッズ': 'wide_1_odds', 'ワイド2_オッズ': 'wide_2_odds', 'ワイド3_オッズ': 'wide_3_odds',
            'ワイド4_オッズ': 'wide_4_odds', 'ワイド5_オッズ': 'wide_5_odds', 'ワイド6_オッズ': 'wide_6_odds', 'ワイド7_オッズ': 'wide_7_odds',
            'ワイド1_人気': 'wide_1_popularity', 'ワイド2_人気': 'wide_2_popularity', 'ワイド3_人気': 'wide_3_popularity',
            'ワイド4_人気': 'wide_4_popularity', 'ワイド5_人気': 'wide_5_popularity', 'ワイド6_人気': 'wide_6_popularity', 'ワイド7_人気': 'wide_7_popularity',

            '馬単1_組合せ1': 'exacta_1_comb1', '馬単1_組合せ2': 'exacta_1_comb2',
            '馬単2_組合せ1': 'exacta_2_comb1', '馬単2_組合せ2': 'exacta_2_comb2',
            '馬単1_オッズ': 'exacta_1_odds', '馬単2_オッズ': 'exacta_2_odds',
            '馬単1_人気': 'exacta_1_popularity', '馬単2_人気': 'exacta_2_popularity',

            '三連複1_組合せ1': 'trio_1_comb1', '三連複1_組合せ2': 'trio_1_comb2', '三連複1_組合せ3': 'trio_1_comb3',
            '三連複2_組合せ1': 'trio_2_comb1', '三連複2_組合せ2': 'trio_2_comb2', '三連複2_組合せ3': 'trio_2_comb3',
            '三連複3_組合せ1': 'trio_3_comb1', '三連複3_組合せ2': 'trio_3_comb2', '三連複3_組合せ3': 'trio_3_comb3',
            '三連複1_オッズ': 'trio_1_odds', '三連複2_オッズ': 'trio_2_odds', '三連複3_オッズ': 'trio_3_odds',
            '三連複1_人気': 'trio_1_popularity', '三連複2_人気': 'trio_2_popularity', '三連複3_人気': 'trio_3_popularity',

            '三連単1_組合せ1': 'trifecta_1_comb1', '三連単1_組合せ2': 'trifecta_1_comb2', '三連単1_組合せ3': 'trifecta_1_comb3',
            '三連単2_組合せ1': 'trifecta_2_comb1', '三連単2_組合せ2': 'trifecta_2_comb2', '三連単2_組合せ3': 'trifecta_2_comb3',
            '三連単3_組合せ1': 'trifecta_3_comb1', '三連単3_組合せ2': 'trifecta_3_comb2', '三連単3_組合せ3': 'trifecta_3_comb3',
            '三連単1_オッズ': 'trifecta_1_odds', '三連単2_オッズ': 'trifecta_2_odds', '三連単3_オッズ': 'trifecta_3_odds',
            '三連単1_人気': 'trifecta_1_popularity', '三連単2_人気': 'trifecta_2_popularity', '三連単3_人気': 'trifecta_3_popularity'
        }
        self.odds.rename(columns=column_map, inplace=True)

    def translate_race_results(self):
        col_map = {
            'レース馬番ID': 'race_pp_id',
            'レースID': 'race_id',
            'レース日付': 'race_date',
            '開催回数': 'race_meeting_no',
            '競馬場コード': 'racecourse_code',
            '競馬場名': 'racecourse_name',
            '開催日数': 'racing_day',
            '競争条件': 'race_cond',
            'レース番号': 'race_no',
            '重賞回次': 'graded_race_no',
            'レース名': 'race_name',
            'リステッド・重賞競走': 'listed_or_graded',

            'レース記号/[抽]': 'symbol_drawn_1',
            'レース記号/(馬齢)': 'symbol_age_restricted',
            'レース記号/牝': 'symbol_female_only',
            'レース記号/(父)': 'symbol_sire_restricted',
            'レース記号/(別定)': 'symbol_set_weight_specific',
            'レース記号/(混)': 'symbol_mixed',
            'レース記号/(ハンデ)': 'symbol_handicap',
            'レース記号/(抽)': 'symbol_drawn_2',
            'レース記号/(市)': 'symbol_market_bought',
            'レース記号/(定量)': 'symbol_level_weight',
            'レース記号/牡': 'symbol_male_only',
            'レース記号/関東配布馬': 'symbol_kanto_distributed',
            'レース記号/(指)': 'symbol_designated_1',
            'レース記号/関西配布馬': 'symbol_kansai_distributed',
            'レース記号/九州産馬': 'symbol_kyushu_bred',
            'レース記号/見習騎手': 'symbol_apprentice_jockey',
            'レース記号/せん': 'symbol_gelding_only',
            'レース記号/(国際)': 'symbol_international',
            'レース記号/[指]': 'symbol_designated_2',
            'レース記号/(特指)': 'symbol_specially_designated',

            '障害区分': 'steeplechase_cat',
            '芝・ダート区分': 'turf_or_dirt',
            '芝・ダート区分2': 'surface_cat_2',
            '右左回り・直線区分': 'track_direction',
            '内・外・襷区分': 'track_path',
            '距離(m)': 'distance',
            '天候': 'weather',
            '馬場状態1': 'track_cond_1',
            '馬場状態2': 'track_cond_2',
            '発走時刻': 'post_time',

            '着順': 'fp',
            '着順注記': 'fp_note',
            '枠番': 'bk',
            '馬番': 'pp',
            '馬名': 'horse_name',
            '性別': 'sex',
            '馬齢': 'age',
            '斤量': 'weight',
            '騎手': 'jockey',
            'タイム': 'total_time',
            '着差': 'margin',
            '1コーナー': 'corner_pos_1',
            '2コーナー': 'corner_pos_2',
            '3コーナー': 'corner_pos_3',
            '4コーナー': 'corner_pos_4',
            '上り': 'l3f',
            '単勝': 'win_odds',
            '人気': 'popularity',
            '馬体重': 'horse_weight',
            '場体重増減': 'horse_weight_diff',

            '東西・外国・地方区分': 'stable_region',
            '調教師': 'trainer',
            '馬主': 'owner',
            '賞金(万円)': 'prize'
        }
        self.race_results.rename(columns=col_map, inplace=True)

        symbol_cols = [col for col in self.race_results.columns if col.startswith('symbol_')]
        for col in symbol_cols:
            self.race_results[col] = self.race_results[col].notna().astype(int)

        entry_map = {
            'sex': {'牡': 'Colt/Stallion', '牝': 'Filly/Mare', 'セ': 'Gelding'},
            'turf_or_dirt': {'芝': 'Turf', 'ダート': 'Dirt'},
            'weather': {
                '晴': 'Fine', '晴 ': 'Fine', '曇': 'Cloudy', '曇 ': 'Cloudy',
                '小雨': 'Light Rain', '小雨 ': 'Light Rain', '雨': 'Rainy',
                '小雪': 'Light Snow', '雪': 'Snowy'
            },
            'track_cond_1': {'良': 'Firm', '稍重': 'Good', '重': 'Yielding', '不良': 'Soft'},
            'track_cond_2': {'良': 'Firm', '稍重': 'Good', '重': 'Yielding', '不良': 'Soft'},
            'track_direction': {'右': 'Right', '左': 'Left', '直線': 'Straight'},
            'track_path': {
                '外': 'Outer', '外-内': 'Outer-to-Inner', '内-外': 'Inner-to-Outer',
                '内2周': 'Inner 2 Laps', '外2周': 'Outer 2 Laps', '襷': 'Chute'
            },
            'stable_region': {'東': 'East', '西': 'West', '地': 'Local', '外': 'Foreign'},
            'fp_note': {
                '取': 'Scratched', '中': 'Stopped', '除': 'Excluded',
                '失': 'Disqualified', '再': 'Remounted', '降': 'Demoted'
            },
            'racecourse_name': {
                '札幌': 'Sapporo', '函館': 'Hakodate', '福島': 'Fukushima',
                '新潟': 'Niigata', '東京': 'Tokyo', '中山': 'Nakayama',
                '中京': 'Chukyo', '京都': 'Kyoto', '阪神': 'Hanshin', '小倉': 'Kokura'
            },
            'surface_cat_2': {
                'ダート': 'Dirt'
            },
            'margin': {
                'ハナ': 'Nose', 'アタマ': 'Head', 'クビ': 'Neck',
                '大': 'Distance', '同着': 'Dead Heat'
            }
        }

        for col, mapping in entry_map.items():
            if col in self.race_results.columns:
                self.race_results[col] = self.race_results[col].replace(mapping)

        margin_sub_map = {
            'ハナ': 'Nose',
            'アタマ': 'Head',
            'クビ': 'Neck',
            '大': 'Distance'
        }

        for jp, en in margin_sub_map.items():
            self.race_results['margin'] = self.race_results['margin'].str.replace(jp, en, regex=False)

        self.race_results['race_cond'] = self.race_results['race_cond'].str.strip()

        self.race_results['steeplechase_cat'] = self.race_results['steeplechase_cat'].fillna('Flat')
        self.race_results.loc[self.race_results['steeplechase_cat'] == '障害', 'steeplechase_cat'] = 'Steeplechase'

        race_cond_map = {
            '3歳新馬': '3yo Newcomer', '4歳新馬': '4yo Newcomer', '2歳新馬': '2yo Newcomer',
            '3歳未勝利': '3yo Maiden', '4歳未勝利': '4yo Maiden', '2歳未勝利': '2yo Maiden',
            '3歳未出走': '3yo Unraced', '4歳未出走': '4yo Unraced',
            '3歳オープン': '3yo Open', '4歳オープン': '4yo Open', '5歳以上オープン': '5yo+ Open',
            '3歳以上オープン': '3yo+ Open', '4歳以上オープン': '4yo+ Open', '2歳オープン': '2yo Open',
            '3歳300万下': '3yo Under 3M', '3歳400万下': '3yo Under 4M', '3歳500万下': '3yo Under 5M',
            '3歳900万下': '3yo Under 9M', '3歳1000万下': '3yo Under 10M',
            '4歳400万下': '4yo Under 4M', '4歳500万下': '4yo Under 5M', '4歳900万下': '4yo Under 9M',
            '2歳500万下': '2yo Under 5M',
            '3歳以上500万下': '3yo+ Under 5M', '3歳以上1000万下': '3yo+ Under 10M',
            '3歳以上1600万下': '3yo+ Under 16M', '4歳以上300万下': '4yo+ Under 3M',
            '4歳以上400万下': '4yo+ Under 4M', '4歳以上500万下': '4yo+ Under 5M',
            '4歳以上600万下': '4yo+ Under 6M', '4歳以上700万下': '4yo+ Under 7M',
            '4歳以上800万下': '4yo+ Under 8M', '4歳以上900万下': '4yo+ Under 9M',
            '4歳以上1000万下': '4yo+ Under 10M', '4歳以上1400万下': '4yo+ Under 14M',
            '4歳以上1500万下': '4yo+ Under 15M', '4歳以上1600万下': '4yo+ Under 16M',
            '2歳1勝クラス': '2yo 1-Win', '3歳1勝クラス': '3yo 1-Win', '3歳以上1勝クラス': '3yo+ 1-Win',
            '4歳以上1勝クラス': '4yo+ 1-Win', '3歳以上2勝クラス': '3yo+ 2-Win',
            '4歳以上2勝クラス': '4yo+ 2-Win', '4歳以上3勝クラス': '4yo+ 3-Win',
            '障害4歳以上未勝利': 'Steeplechase 4yo+ Maiden', '障害3歳以上未勝利': 'Steeplechase 3yo+ Maiden',
            '障害4歳以上オープン': 'Steeplechase 4yo+ Open', '障害3歳以上オープン': 'Steeplechase 3yo+ Open',
            '障害4歳以上400万下': 'Steeplechase 4yo+ Under 4M'
        }

        self.race_results['race_cond'] = self.race_results['race_cond'].replace(race_cond_map)
