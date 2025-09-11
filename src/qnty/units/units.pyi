"""Type stubs for field units."""

from .core import Unit, UnitRegistry


class AbsorbedDoseUnits:
    """Unit constants for Absorbed Radiation Dose."""
    __slots__: tuple[()]

    erg_per_gram: Unit
    erg_g: Unit
    erg_per_g: Unit
    gram_rad: Unit
    g_rad: Unit
    gray: Unit
    Gy: Unit
    rad: Unit

class AccelerationUnits:
    """Unit constants for Acceleration."""
    __slots__: tuple[()]

    meter_per_second_squared: Unit
    mathrm_m_mathrm_s_2: Unit
    m_per_s2: Unit
    foot_per_second_squared: Unit
    mathrm_ft_mathrm_s_2_or_mathrm_ft_mathrm_sec_2: Unit
    ft_per_s2: Unit
    fps2: Unit

class ActivationEnergyUnits:
    """Unit constants for Activation Energy."""
    __slots__: tuple[()]

    btu_per_pound_mole: Unit
    Btu_lb_mol: Unit
    btu_per_lbmol: Unit
    calorie_mean_per_gram_mole: Unit
    cal_mol: Unit
    cal_mean_per_gmol: Unit
    joule_per_gram_mole: Unit
    J_mol: Unit
    joule_per_kilogram_mole: Unit
    J_kmol: Unit
    kilocalorie_per_kilogram_mole: Unit
    kcal_kmol: Unit

class AmountOfSubstanceUnits:
    """Unit constants for Amount of Substance."""
    __slots__: tuple[()]

    kilogram_mol: Unit
    kmol: Unit
    mole: Unit
    mol: Unit
    pound_mole: Unit
    lb_mol_or_mole: Unit
    lb_mol: Unit

class AnglePlaneUnits:
    """Unit constants for Angle, Plane."""
    __slots__: tuple[()]

    degree: Unit
    circ: Unit
    gon: Unit
    grade: Unit
    minute_new: Unit
    c: Unit
    minute_of_angle: Unit
    unnamed: Unit
    percent: Unit
    plane_angle: Unit
    quadrant: Unit
    quadr: Unit
    radian: Unit
    right_angle: Unit
    perp: Unit
    round: Unit
    tr_or_r: Unit
    tr: Unit
    r: Unit
    second_new: Unit
    cc: Unit
    second_of_angle: Unit
    thousandth_us: Unit
    US: Unit
    turn: Unit
    turn_or_rev: Unit
    rev: Unit

class AngleSolidUnits:
    """Unit constants for Angle, Solid."""
    __slots__: tuple[()]

    spat: Unit
    square_degree: Unit
    left_circ_right_2: Unit
    square_gon: Unit
    g_2: Unit
    steradian: Unit
    sr: Unit

class AngularAccelerationUnits:
    """Unit constants for Angular Acceleration."""
    __slots__: tuple[()]

    radian_per_second_squared: Unit
    mathrm_rad_mathrm_s_2: Unit
    revolution_per_second_squared: Unit
    mathrm_rev_mathrm_sec_2: Unit
    rpm_or_revolution_per_minute: Unit
    mathrm_rev_mathrm_min_2_or_rpm_min: Unit
    rev_min_2: Unit
    rpm_min: Unit

class AngularMomentumUnits:
    """Unit constants for Angular Momentum."""
    __slots__: tuple[()]

    gram_centimeter_squared_per_second: Unit
    mathrm_g_mathrm_cm_2_mathrm_s: Unit
    kilogram_meter_squared_per_second: Unit
    mathrm_kg_mathrm_m_2_mathrm_s: Unit
    pound_force_square_foot_per_second: Unit
    lb_ft_2_mathrm_sec: Unit

class AreaUnits:
    """Unit constants for Area."""
    __slots__: tuple[()]

    acre_general: Unit
    ac: Unit
    are: Unit
    a: Unit
    arpent_quebec: Unit
    arp: Unit
    barn: Unit
    b: Unit
    circular_inch: Unit
    cin: Unit
    circular_mil: Unit
    cmil: Unit
    hectare: Unit
    ha: Unit
    shed: Unit
    square_centimeter: Unit
    mathrm_cm_2: Unit
    square_chain_ramsden: Unit
    sq_ch_Rams: Unit
    square_chain_survey_gunters: Unit
    sq_ch_surv: Unit
    square_decimeter: Unit
    mathrm_dm_2: Unit
    square_fermi: Unit
    mathrm_F_2: Unit
    square_foot: Unit
    sq_ft_or_ft_2: Unit
    sq_ft: Unit
    ft_2: Unit
    square_hectometer: Unit
    mathrm_hm_2: Unit
    square_inch: Unit
    sq_in_or_in_2: Unit
    sq_in: Unit
    in_2: Unit
    square_kilometer: Unit
    mathrm_km_2: Unit
    square_league_statute: Unit
    sq_lg_stat: Unit
    square_meter: Unit
    mathrm_m_2: Unit
    square_micron: Unit
    mu_mathrm_m_2_or_mu_2: Unit
    mu_m_2: Unit
    mu_2: Unit
    square_mile_statute: Unit
    sq_mi_stat: Unit
    square_mile_us_survey: Unit
    sq_mi_US_Surv: Unit
    square_millimeter: Unit
    mathrm_mm_2: Unit
    square_nanometer: Unit
    mathrm_nm_2: Unit
    square_yard: Unit
    sq_yd: Unit
    township_us: Unit
    twshp: Unit

class AreaPerUnitVolumeUnits:
    """Unit constants for Area per Unit Volume."""
    __slots__: tuple[()]

    square_centimeter_per_cubic_centimeter: Unit
    mathrm_cm_2_mathrm_cc: Unit
    square_foot_per_cubic_foot: Unit
    mathrm_ft_2_mathrm_ft_3_or_sqft_cft: Unit
    ft_2_ft_3: Unit
    sqft_cft: Unit
    square_inch_per_cubic_inch: Unit
    mathrm_in_2_mathrm_in_3_or_sq_in_cu_in: Unit
    in_2_in_3: Unit
    sq_in_cu_in: Unit
    square_meter_per_cubic_meter: Unit
    mathrm_m_2_mathrm_m_3_or_1_mathrm_m_3: Unit
    m_2_m_3: Unit
    unit_1_m_3: Unit

class AtomicWeightUnits:
    """Unit constants for Atomic Weight."""
    __slots__: tuple[()]

    atomic_mass_unit_12c: Unit
    amu: Unit
    grams_per_mole: Unit
    g_mol: Unit
    kilograms_per_kilomole: Unit
    kg_kmol: Unit
    pounds_per_pound_mole: Unit
    mathrm_lb_mathrm_lb_mol_or_mathrm_lb_mole: Unit
    lb_lb_mol: Unit
    lb_mole: Unit

class ConcentrationUnits:
    """Unit constants for Concentration."""
    __slots__: tuple[()]

    grains_of_i_per_cubic_foot: Unit
    mathrm_gr_mathrm_ft_3_or_gr_cft: Unit
    gr_ft_3: Unit
    gr_cft: Unit
    grains_of_i_per_gallon_us: Unit
    gr_gal: Unit

class DimensionlessUnits:
    """Unit constants for Dimensionless."""
    __slots__: tuple[()]

    dimensionless: Unit
    ratio: Unit
    parts_per_million: Unit
    ppm: Unit
    parts_per_billion: Unit
    ppb: Unit

class DynamicFluidityUnits:
    """Unit constants for Dynamic Fluidity."""
    __slots__: tuple[()]

    meter_seconds_per_kilogram: Unit
    m_s_kg: Unit
    rhe: Unit
    square_foot_per_pound_second: Unit
    mathrm_ft_2_lb_sec: Unit
    square_meters_per_newton_per_second: Unit
    mathrm_m_2_mathrm_N_mathrm_s: Unit

class ElectricCapacitanceUnits:
    """Unit constants for Electric Capacitance."""
    __slots__: tuple[()]

    cm: Unit
    abfarad: Unit
    emu_cgs: Unit
    farad: Unit
    F: Unit
    farad_intl: Unit
    F_int: Unit
    jar: Unit
    puff: Unit
    statfarad: Unit
    esu_cgs: Unit

class ElectricChargeUnits:
    """Unit constants for Electric Charge."""
    __slots__: tuple[()]

    abcoulomb: Unit
    ampere_hour: Unit
    Ah: Unit
    coulomb: Unit
    C: Unit
    faraday_c12: Unit
    franklin: Unit
    Fr: Unit
    statcoulomb: Unit
    u_a_charge: Unit
    u_a: Unit

class ElectricCurrentIntensityUnits:
    """Unit constants for Electric Current Intensity."""
    __slots__: tuple[()]

    abampere: Unit
    ampere_intl_mean: Unit
    A_int_mean: Unit
    ampere_intl_us: Unit
    A_int_US: Unit
    ampere_or_amp: Unit
    A: Unit
    biot: Unit
    statampere: Unit
    u_a_or_current: Unit

class ElectricDipoleMomentUnits:
    """Unit constants for Electric Dipole Moment."""
    __slots__: tuple[()]

    ampere_meter_second: Unit
    A_m_s: Unit
    coulomb_meter: Unit
    C_m: Unit
    debye: Unit
    D: Unit
    electron_meter: Unit
    e_m: Unit

class ElectricFieldStrengthUnits:
    """Unit constants for Electric Field Strength."""
    __slots__: tuple[()]

    volt_per_centimeter: Unit
    V_cm: Unit
    volt_per_meter: Unit
    V_m: Unit

class ElectricInductanceUnits:
    """Unit constants for Electric Inductance."""
    __slots__: tuple[()]

    abhenry: Unit
    cm: Unit
    henry: Unit
    H: Unit
    henry_intl_mean: Unit
    H_int_mean: Unit
    henry_intl_us: Unit
    H_int_US: Unit
    mic: Unit
    stathenry: Unit

class ElectricPotentialUnits:
    """Unit constants for Electric Potential."""
    __slots__: tuple[()]

    abvolt: Unit
    statvolt: Unit
    u_a_potential: Unit
    volt: Unit
    V: Unit
    volt_intl_mean: Unit
    V_int_mean: Unit
    volt_us: Unit
    V_int_US: Unit

class ElectricResistanceUnits:
    """Unit constants for Electric Resistance."""
    __slots__: tuple[()]

    abohm: Unit
    jacobi: Unit
    lenz: Unit
    Metric: Unit
    ohm: Unit
    Omega: Unit
    ohm_intl_mean: Unit
    Omega_int_mean: Unit
    ohm_intl_us: Unit
    Omega_int_US: Unit
    ohm_legal: Unit
    Omega_legal: Unit
    preece: Unit
    statohm: Unit
    csu_cgs: Unit
    wheatstone: Unit

class ElectricalConductanceUnits:
    """Unit constants for Electrical Conductance."""
    __slots__: tuple[()]

    emu_cgs: Unit
    esu_cgs: Unit
    mho: Unit
    microsiemens: Unit
    mu_mathrm_S: Unit
    siemens: Unit
    S: Unit

class ElectricalPermittivityUnits:
    """Unit constants for Electrical Permittivity."""
    __slots__: tuple[()]

    farad_per_meter: Unit
    F_m: Unit

class ElectricalResistivityUnits:
    """Unit constants for Electrical Resistivity."""
    __slots__: tuple[()]

    circular_mil_ohm_per_foot: Unit
    circmil_Omega_mathrm_ft: Unit
    emu_cgs: Unit
    microhm_inch: Unit
    mu_Omega_in: Unit
    ohm_centimeter: Unit
    boldsymbol_Omega_mathbf_c_m: Unit
    ohm_meter: Unit
    Omega_mathrm_m: Unit

class EnergyFluxUnits:
    """Unit constants for Energy Flux."""
    __slots__: tuple[()]

    btu_per_square_foot_per_hour: Unit
    mathrm_Btu_mathrm_ft_2_mathrm_hr: Unit
    calorie_per_square_centimeter_per_second: Unit
    mathrm_cal_mathrm_cm_2_mathrm_s_or_mathrm_cal_mathrm_cm_2_mathrm_s: Unit
    cal_cm_2_s: Unit
    celsius_heat_units_chu: Unit
    mathrm_Chu_mathrm_ft_2_mathrm_hr: Unit
    kilocalorie_per_square_foot_per_hour: Unit
    mathrm_kcal_left_mathrm_ft_2_mathrm_hr_right: Unit
    kilocalorie_per_square_meter_per_hour: Unit
    mathrm_kcal_left_mathrm_m_2_mathrm_hr_right: Unit
    watt_per_square_meter: Unit
    mathrm_W_mathrm_m_2: Unit

class EnergyHeatWorkUnits:
    """Unit constants for Energy, Heat, Work."""
    __slots__: tuple[()]

    barrel_oil_equivalent_or_equivalent_barrel: Unit
    bboe_or_boe: Unit
    bboe: Unit
    boe: Unit
    billion_electronvolt: Unit
    BeV: Unit
    british_thermal_unit_4circ_mathrmc: Unit
    Btu_39_2_circ_mathrm_F: Unit
    british_thermal_unit_60circ_mathrmf: Unit
    Btu_60_circ_mathrm_F: Unit
    british_thermal_unit_international_steam_tables: Unit
    Btu_IT: Unit
    british_thermal_unit_isotc_12: Unit
    Btu_ISO: Unit
    british_thermal_unit_mean: Unit
    Btu_mean_or_Btu: Unit
    Btu_mean: Unit
    Btu: Unit
    british_thermal_unit_thermochemical: Unit
    Btu_therm: Unit
    calorie_20circ_mathrmc: Unit
    cal_20_circ_mathrm_C: Unit
    calorie_4circ_mathrmc: Unit
    cal_4_circ_mathrm_C: Unit
    calorie_international_steam_tables: Unit
    cal_IT: Unit
    calorie_mean: Unit
    cal_mean: Unit
    calorie_nutritional: Unit
    Cal_nutr: Unit
    calorie_thermochemical: Unit
    cal_therm: Unit
    celsius_heat_unit: Unit
    Chu: Unit
    celsius_heat_unit_15_circ_mathrmc: Unit
    Chu_15_circ_mathrm_C: Unit
    electron_volt: Unit
    eV: Unit
    erg: Unit
    foot_pound_force_duty: Unit
    ft_mathrm_lb_mathrm_f: Unit
    foot_poundal: Unit
    ft_pdl: Unit
    frigorie: Unit
    fg: Unit
    hartree_atomic_unit_of_energy: Unit
    mathrm_E_mathrm_H_a_u: Unit
    joule: Unit
    J: Unit
    joule_international: Unit
    J_intl: Unit
    kilocalorie_thermal: Unit
    kcal_therm: Unit
    kilogram_force_meter: Unit
    mathrm_kg_mathrm_f_m: Unit
    kiloton_tnt: Unit
    kt_TNT: Unit
    kilowatt_hour: Unit
    kWh: Unit
    liter_atmosphere: Unit
    L_atm: Unit
    megaton_tnt: Unit
    Mt_TNT: Unit
    pound_centigrade_unit_15circ_mathrmc: Unit
    pcu_15_circ_mathrm_C: Unit
    prout: Unit
    q_unit: Unit
    Q: Unit
    quad_quadrillion_btu: Unit
    quad: Unit
    rydberg: Unit
    Ry: Unit
    therm_eeg: Unit
    therm_EEG: Unit
    therm_refineries: Unit
    therm_refy_or_therm: Unit
    therm_refy: Unit
    therm: Unit
    therm_us: Unit
    therm_US_or_therm: Unit
    ton_coal_equivalent: Unit
    tce_tec: Unit
    ton_oil_equivalent: Unit
    toe_tep: Unit

class EnergyPerUnitAreaUnits:
    """Unit constants for Energy per Unit Area."""
    __slots__: tuple[()]

    british_thermal_unit_per_square_foot: Unit
    mathrm_Btu_mathrm_ft_2_or_Btu_sq_ft: Unit
    Btu_ft_2: Unit
    Btu_sq_ft: Unit
    joule_per_square_meter: Unit
    mathrm_J_mathrm_m_2: Unit
    langley: Unit
    Ly: Unit

class ForceUnits:
    """Unit constants for Force."""
    __slots__: tuple[()]

    crinal: Unit
    dyne: Unit
    dyn: Unit
    funal: Unit
    kilogram_force: Unit
    mathrm_kg_mathrm_f: Unit
    kip_force: Unit
    operatorname_kip_mathrm_f: Unit
    newton: Unit
    N: Unit
    ounce_force: Unit
    mathrm_oz_mathrm_f_or_oz: Unit
    oz_f: Unit
    oz: Unit
    pond: Unit
    p: Unit
    pound_force: Unit
    mathrm_lb_mathrm_f_or_lb: Unit
    lb_f: Unit
    lb: Unit
    poundal: Unit
    pdl: Unit
    slug_force: Unit
    operatorname_slug_f: Unit
    sth_ne: Unit
    sn: Unit
    ton_force_long: Unit
    LT: Unit
    ton_force_metric: Unit
    MT: Unit
    ton_force_short: Unit
    T: Unit

class ForceBodyUnits:
    """Unit constants for Force (Body)."""
    __slots__: tuple[()]

    dyne_per_cubic_centimeter: Unit
    dyn_cc_or_dyn_mathrm_cm_3: Unit
    dyn_cc: Unit
    dyn_cm_3: Unit
    kilogram_force_per_cubic_centimeter: Unit
    mathrm_kg_mathrm_f_mathrm_cm_3: Unit
    kilogram_force_per_cubic_meter: Unit
    mathrm_kg_mathrm_f_mathrm_m_3: Unit
    newton_per_cubic_meter: Unit
    mathrm_N_mathrm_m_3: Unit
    pound_force_per_cubic_foot: Unit
    mathrm_lb_mathrm_f_mathrm_cft: Unit
    pound_force_per_cubic_inch: Unit
    mathrm_lb_mathrm_f_mathrm_cu_mathrm_in: Unit
    ton_force_per_cubic_foot: Unit
    ton_mathrm_f_mathrm_cft: Unit

class ForcePerUnitMassUnits:
    """Unit constants for Force per Unit Mass."""
    __slots__: tuple[()]

    dyne_per_gram: Unit
    dyn_g: Unit
    kilogram_force_per_kilogram: Unit
    mathrm_kg_mathrm_f_mathrm_kg: Unit
    newton_per_kilogram: Unit
    N_kg: Unit
    pound_force_per_pound_mass: Unit
    mathrm_lb_mathrm_f_mathrm_lb_or_mathrm_lb_mathrm_f_mathrm_lb_mathrm_m: Unit
    lb_f_lb: Unit
    lb_f_lb_m: Unit
    pound_force_per_slug: Unit
    mathrm_lb_mathrm_f_slug: Unit

class FrequencyVoltageRatioUnits:
    """Unit constants for Frequency Voltage Ratio."""
    __slots__: tuple[()]

    cycles_per_second_per_volt: Unit
    cycle_sec_V: Unit
    hertz_per_volt: Unit
    Hz_V: Unit
    terahertz_per_volt: Unit
    THz_V: Unit

class FuelConsumptionUnits:
    """Unit constants for Fuel Consumption."""
    __slots__: tuple[()]

    unit_100_km_per_liter: Unit
    gallons_uk: Unit
    gal_UK_100_mi: Unit
    gallons_us: Unit
    gal_US_100_mi: Unit
    kilometers_per_gallon_uk: Unit
    km_gal_UK: Unit
    kilometers_per_gallon_us: Unit
    km_gal_US: Unit
    kilometers_per_liter: Unit
    km_l: Unit
    liters_per_100_km: Unit
    liters_per_kilometer: Unit
    unit_1_km: Unit
    meters_per_gallon_uk: Unit
    m_gal_UK: Unit
    meters_per_gallon_us: Unit
    unit_1_gal_US: Unit
    miles_per_gallon_uk: Unit
    mi_gal_UK_or_mpg_UK: Unit
    mi_gal_UK: Unit
    mpg_UK: Unit
    miles_per_gallon_us: Unit
    mi_gal_US_or_mpg_US: Unit
    mi_gal_US: Unit
    mpg_US: Unit
    miles_per_liter: Unit
    mi_l: Unit

class HeatOfCombustionUnits:
    """Unit constants for Heat of Combustion."""
    __slots__: tuple[()]

    british_thermal_unit_per_pound: Unit
    Btu_lb: Unit
    calorie_per_gram: Unit
    mathrm_cal_mathrm_g: Unit
    chu_per_pound: Unit
    Chu_lb: Unit
    joule_per_kilogram: Unit
    J_kg: Unit

class HeatOfFusionUnits:
    """Unit constants for Heat of Fusion."""
    __slots__: tuple[()]

    british_thermal_unit_mean: Unit
    british_thermal_unit_per_pound: Unit
    calorie_per_gram: Unit
    chu_per_pound: Unit
    joule_per_kilogram: Unit

class HeatOfVaporizationUnits:
    """Unit constants for Heat of Vaporization."""
    __slots__: tuple[()]

    british_thermal_unit_per_pound: Unit
    calorie_per_gram: Unit
    chu_per_pound: Unit
    joule_per_kilogram: Unit

class HeatTransferCoefficientUnits:
    """Unit constants for Heat Transfer Coefficient."""
    __slots__: tuple[()]

    btu_per_square_foot_per_hour_per_degree_fahrenheit_or_rankine: Unit
    mathrm_Btu_left_mathrm_ft_2_mathrm_h_circ_mathrm_F_right: Unit
    watt_per_square_meter_per_degree_celsius_or_kelvin: Unit
    mathrm_W_left_mathrm_m_2_circ_mathrm_C_right: Unit

class IlluminanceUnits:
    """Unit constants for Illuminance."""
    __slots__: tuple[()]

    foot_candle: Unit
    mathrm_ft_mathrm_C_or_mathrm_ft_mathrm_Cd: Unit
    ft_C: Unit
    ft_Cd: Unit
    lux: Unit
    lx: Unit
    nox: Unit
    phot: Unit
    ph: Unit
    skot: Unit

class KineticEnergyOfTurbulenceUnits:
    """Unit constants for Kinetic Energy of Turbulence."""
    __slots__: tuple[()]

    square_foot_per_second_squared: Unit
    mathrm_ft_2_mathrm_s_2_or_sqft_sec_2: Unit
    ft_2_s_2: Unit
    sqft_sec_2: Unit
    square_meters_per_second_squared: Unit
    mathrm_m_2_mathrm_s_2: Unit

class LengthUnits:
    """Unit constants for Length."""
    __slots__: tuple[()]

    ngstr_m: Unit
    AA: Unit
    arpent_quebec: Unit
    astronomic_unit: Unit
    AU: Unit
    attometer: Unit
    am: Unit
    calibre_centinch: Unit
    centimeter: Unit
    chain_engrs_or_ramsden: Unit
    ch_eng_or_Rams: Unit
    ch_eng: Unit
    Rams: Unit
    chain_gunters: Unit
    ch_Gunt: Unit
    chain_surveyors: Unit
    ch_surv: Unit
    cubit_uk: Unit
    cu_UK: Unit
    ell: Unit
    fathom: Unit
    fath: Unit
    femtometre: Unit
    fm: Unit
    fermi: Unit
    foot: Unit
    ft: Unit
    furlong_uk_and_us: Unit
    fur: Unit
    inch: Unit
    in_unit: Unit
    kilometer: Unit
    km: Unit
    league_us_statute: Unit
    lg_US_stat: Unit
    lieue_metric: Unit
    ligne_metric: Unit
    line_us: Unit
    li_US: Unit
    link_surveyors: Unit
    li_surv: Unit
    meter: Unit
    m: Unit
    micrometer: Unit
    mu_mathrm_m: Unit
    micron: Unit
    mu: Unit
    mil: Unit
    mile_geographical: Unit
    mi_geog: Unit
    mile_us_nautical: Unit
    mi_US_naut: Unit
    mile_us_statute: Unit
    mi_us: Unit
    mile_us_survey: Unit
    mi_US_surv: Unit
    millimeter: Unit
    mm: Unit
    millimicron: Unit
    mathrm_m_mu: Unit
    nanometer_or_nanon: Unit
    nm: Unit
    parsec: Unit
    pc: Unit
    perche: Unit
    rod: Unit
    pica: Unit
    picometer: Unit
    pm: Unit
    point_didot: Unit
    pt_Didot: Unit
    point_us: Unit
    pt_US: Unit
    rod_or_pole: Unit
    span: Unit
    thou_millinch: Unit
    thou: Unit
    toise_metric: Unit
    yard: Unit
    yd: Unit

class LinearMassDensityUnits:
    """Unit constants for Linear Mass Density."""
    __slots__: tuple[()]

    denier: Unit
    kilogram_per_centimeter: Unit
    kg_cm: Unit
    kilogram_per_meter: Unit
    kg_m: Unit
    pound_per_foot: Unit
    lb_ft: Unit
    pound_per_inch: Unit
    lb_in: Unit
    pound_per_yard: Unit
    lb_yd: Unit
    ton_metric_km: Unit
    t_km_or_MT_km: Unit
    t_km: Unit
    MT_km: Unit
    ton_metric_m: Unit
    t_m_or_MT_m: Unit
    t_m: Unit
    MT_m: Unit

class LinearMomentumUnits:
    """Unit constants for Linear Momentum."""
    __slots__: tuple[()]

    foot_pounds_force_per_hour: Unit
    mathrm_ft_mathrm_lb_mathrm_f_mathrm_h_or_mathrm_ft_mathrm_lb_mathrm_hr: Unit
    ft_lb_f_h: Unit
    ft_lb_hr: Unit
    foot_pounds_force_per_minute: Unit
    mathrm_ft_mathrm_lb_mathrm_f_min_or_mathrm_ft_mathrm_lb_min: Unit
    ft_lb_f_min: Unit
    ft_lb_min: Unit
    foot_pounds_force_per_second: Unit
    mathrm_ft_mathrm_lb_mathrm_f_mathrm_s_or_ft_lb_sec: Unit
    ft_lb_f_s: Unit
    ft_lb_sec: Unit
    gram_centimeters_per_second: Unit
    mathrm_g_mathrm_cm_mathrm_s: Unit
    kilogram_meters_per_second: Unit
    mathrm_kg_mathrm_m_mathrm_s: Unit

class LuminanceSelfUnits:
    """Unit constants for Luminance (self)."""
    __slots__: tuple[()]

    apostilb: Unit
    asb: Unit
    blondel: Unit
    B1: Unit
    candela_per_square_meter: Unit
    mathrm_cd_mathrm_m_2: Unit
    foot_lambert: Unit
    ft_L: Unit
    lambert: Unit
    L: Unit
    luxon: Unit
    nit: Unit
    stilb: Unit
    sb: Unit
    troland: Unit

class LuminousFluxUnits:
    """Unit constants for Luminous Flux."""
    __slots__: tuple[()]

    candela_steradian: Unit
    cd_sr: Unit
    lumen: Unit

class LuminousIntensityUnits:
    """Unit constants for Luminous Intensity."""
    __slots__: tuple[()]

    candela: Unit
    cd: Unit
    candle_international: Unit
    Cd_int: Unit
    carcel: Unit
    hefner_unit: Unit
    HK: Unit

class MagneticFieldUnits:
    """Unit constants for Magnetic Field."""
    __slots__: tuple[()]

    ampere_per_meter: Unit
    A_m: Unit
    lenz: Unit
    oersted: Unit
    Oe: Unit
    praoersted: Unit

class MagneticFluxUnits:
    """Unit constants for Magnetic Flux."""
    __slots__: tuple[()]

    kapp_line: Unit
    line: Unit
    maxwell: Unit
    Mx: Unit
    unit_pole: Unit
    weber: Unit
    Wb: Unit

class MagneticInductionFieldStrengthUnits:
    """Unit constants for Magnetic Induction Field Strength."""
    __slots__: tuple[()]

    gamma: Unit
    gauss: Unit
    G: Unit
    line_per_square_centimeter: Unit
    line_mathrm_cm_2: Unit
    maxwell_per_square_centimeter: Unit
    mathrm_Mx_mathrm_cm_2: Unit
    tesla: Unit
    u_a: Unit
    weber_per_square_meter: Unit
    mathrm_Wb_mathrm_m_2: Unit

class MagneticMomentUnits:
    """Unit constants for Magnetic Moment."""
    __slots__: tuple[()]

    bohr_magneton: Unit
    Bohr_magneton: Unit
    joule_per_tesla: Unit
    J_T: Unit
    nuclear_magneton: Unit
    nucl_Magneton: Unit

class MagneticPermeabilityUnits:
    """Unit constants for Magnetic Permeability."""
    __slots__: tuple[()]

    henrys_per_meter: Unit
    H_m: Unit
    newton_per_square_ampere: Unit
    N_A_2: Unit

class MagnetomotiveForceUnits:
    """Unit constants for Magnetomotive Force."""
    __slots__: tuple[()]

    abampere_turn: Unit
    ampere: Unit
    ampere_turn: Unit
    A_turn: Unit
    gilbert: Unit
    Gb: Unit

class MassUnits:
    """Unit constants for Mass."""
    __slots__: tuple[()]

    slug: Unit
    sl: Unit
    atomic_mass_unit_12_mathrmc: Unit
    mathrm_u_left_12_mathrm_C_right_or_amu: Unit
    uleft_12_Cright: Unit
    carat_metric: Unit
    ct: Unit
    cental: Unit
    sh_cwt_cH: Unit
    centigram: Unit
    cg: Unit
    clove_uk: Unit
    cl: Unit
    drachm_apothecary: Unit
    dr_ap: Unit
    dram_avoirdupois: Unit
    dr_av: Unit
    dram_troy: Unit
    dr_troy: Unit
    grain: Unit
    gr: Unit
    gram: Unit
    g: Unit
    hundredweight_long_or_gross: Unit
    cwt_lg_cwt: Unit
    hundredweight_short_or_net: Unit
    sh_cwt: Unit
    kilogram: Unit
    kg: Unit
    kip: Unit
    microgram: Unit
    mu_mathrm_g: Unit
    milligram: Unit
    mg: Unit
    ounce_apothecary: Unit
    oz_ap: Unit
    ounce_avoirdupois: Unit
    ounce_troy: Unit
    oz_troy: Unit
    pennyweight_troy: Unit
    dwt_troy: Unit
    pood_russia: Unit
    pood: Unit
    pound_apothecary: Unit
    lb_ap: Unit
    pound_avoirdupois: Unit
    lb_av: Unit
    pound_troy: Unit
    lb_troy: Unit
    pound_mass: Unit
    mathrm_lb_mathrm_m: Unit
    quarter_uk: Unit
    qt: Unit
    quintal_metric: Unit
    q_dt: Unit
    quital_us: Unit
    quint_US: Unit
    scruple_avoirdupois: Unit
    scf: Unit
    stone_uk: Unit
    st: Unit
    ton_metric: Unit
    t: Unit
    ton_us_long: Unit
    lg_ton: Unit
    ton_us_short: Unit
    sh_ton: Unit

class MassDensityUnits:
    """Unit constants for Mass Density."""
    __slots__: tuple[()]

    gram_per_cubic_centimeter: Unit
    g_cc_or_g_ml: Unit
    g_cc: Unit
    g_ml: Unit
    gram_per_cubic_decimeter: Unit
    mathrm_g_mathrm_dm_3: Unit
    gram_per_cubic_meter: Unit
    mathrm_g_mathrm_m_3: Unit
    gram_per_liter: Unit
    mathrm_g_mathrm_l_or_g_L: Unit
    g_l: Unit
    g_L: Unit
    kilogram_per_cubic_meter: Unit
    mathrm_kg_mathrm_m_3: Unit
    ounce_avdp: Unit
    oz_gal: Unit
    pound_avdp: Unit
    mathrm_lb_mathrm_cu_mathrm_ft_or_lb_ft_3: Unit
    lb_cu_ft: Unit
    lb_ft_3: Unit
    pound_avdp: Unit
    pound_mass: Unit
    ton_metric_m3: Unit
    mathrm_t_mathrm_m_3_or_MT_mathrm_m_3: Unit
    t_m_3: Unit
    MT_m_3: Unit

class MassFlowRateUnits:
    """Unit constants for Mass Flow Rate."""
    __slots__: tuple[()]

    kilograms_per_day: Unit
    kg_d: Unit
    kilograms_per_hour: Unit
    kg_h: Unit
    kilograms_per_minute: Unit
    kg_min: Unit
    kilograms_per_second: Unit
    kg_s: Unit
    metric_tons_per_day: Unit
    MT_d_or_MTD: Unit
    MT_d: Unit
    MTD: Unit
    metric_tons_per_hour: Unit
    MT_h_or_MTD: Unit
    MT_h: Unit
    metric_tons_per_minute: Unit
    metric_tons_per_second: Unit
    MT_s: Unit
    metric_tons_per_year_365_d: Unit
    MT_yr_or_MTY: Unit
    MT_yr: Unit
    MTY: Unit
    pounds_per_day: Unit
    mathrm_lb_mathrm_d_or_mathrm_lb_mathrm_da_or_PPD: Unit
    lb_d: Unit
    lb_da: Unit
    PPD: Unit
    pounds_per_hour: Unit
    mathrm_lb_mathrm_h_or_lb_hr_or_PPH: Unit
    lb_h: Unit
    lb_hr: Unit
    PPH: Unit
    pounds_per_minute: Unit
    mathrm_lb_mathrm_min_or_PPM: Unit
    lb_min: Unit
    PPM: Unit
    pounds_per_second: Unit
    mathrm_lb_mathrm_s_or_lb_sec_or_PPS: Unit
    lb_s: Unit
    lb_sec: Unit
    PPS: Unit

class MassFluxUnits:
    """Unit constants for Mass Flux."""
    __slots__: tuple[()]

    kilogram_per_square_meter_per_day: Unit
    mathrm_kg_left_mathrm_m_2_mathrm_d_right: Unit
    kilogram_per_square_meter_per_hour: Unit
    mathrm_kg_left_mathrm_m_2_mathrm_h_right: Unit
    kilogram_per_square_meter_per_minute: Unit
    mathrm_kg_left_mathrm_m_2_mathrm_min_right: Unit
    kilogram_per_square_meter_per_second: Unit
    mathrm_kg_left_mathrm_m_2_mathrm_s_right: Unit
    pound_per_square_foot_per_day: Unit
    mathrm_lb_left_mathrm_ft_2_mathrm_d_right_or_lb_sqft_da: Unit
    lb_left_ft_2_dright: Unit
    lb_sqft_da: Unit
    pound_per_square_foot_per_hour: Unit
    mathrm_lb_left_mathrm_ft_2_mathrm_h_right_or_lb_sqft_hr: Unit
    lb_left_ft_2_hright: Unit
    lb_sqft_hr: Unit
    pound_per_square_foot_per_minute: Unit
    mathrm_lb_left_mathrm_ft_2_min_right_or_lb_sqft_min: Unit
    lb_left_ft_2_min_right: Unit
    lb_sqft_min: Unit
    pound_per_square_foot_per_second: Unit
    mathrm_lb_left_mathrm_ft_2_mathrm_s_right_or_lb_sqft_sec: Unit
    lb_left_ft_2_sright: Unit
    lb_sqft_sec: Unit

class MassFractionOfIUnits:
    """Unit constants for Mass Fraction of "i"."""
    __slots__: tuple[()]

    grains_of_i_per_pound_total: Unit
    mathrm_gr_mathrm_i_mathrm_lb: Unit
    gram_of_i_per_kilogram_total: Unit
    mathrm_g_mathrm_i_mathrm_kg: Unit
    kilogram_of_i_per_kilogram_total: Unit
    mathrm_kg_mathrm_i_mathrm_kg: Unit
    pound_of_i_per_pound_total: Unit
    mathrm_lb_mathrm_i_mathrm_lb: Unit

class MassTransferCoefficientUnits:
    """Unit constants for Mass Transfer Coefficient."""
    __slots__: tuple[()]

    gram_per_square_centimeter_per_second: Unit
    kilogram_per_square_meter_per_second: Unit
    pounds_force_per_cubic_foot_per_hour: Unit
    mathrm_lb_mathrm_f_mathrm_ft_3_mathrm_h_or_mathrm_lb_mathrm_f_mathrm_cft_mathrm_hr: Unit
    lb_f_ft_3_h: Unit
    lb_f_cft_hr: Unit
    pounds_mass_per_square_foot_per_hour: Unit
    lb_ft_2_mathrm_hr_or_lb_sqft_hr: Unit
    lb_ft_2_hr: Unit
    pounds_mass_per_square_foot_per_second: Unit

class MolalityOfSoluteIUnits:
    """Unit constants for Molality of Solute "i"."""
    __slots__: tuple[()]

    gram_moles_of_i_per_kilogram: Unit
    mathrm_mol_mathrm_i_mathrm_kg: Unit
    kilogram_mols_of_i_per_kilogram: Unit
    mathrm_kmol_mathrm_i_mathrm_kg: Unit
    kmols_of_i_per_kilogram: Unit
    mols_of_i_per_gram: Unit
    mathrm_mol_mathrm_i_mathrm_g: Unit
    pound_moles_of_i_per_pound_mass: Unit
    mole_mathrm_i_mathrm_lb_mass: Unit

class MolarConcentrationByMassUnits:
    """Unit constants for Molar Concentration by Mass."""
    __slots__: tuple[()]

    gram_mole_or_mole_per_gram: Unit
    mol_g: Unit
    gram_mole_or_mole_per_kilogram: Unit
    mol_kg: Unit
    kilogram_mole_or_kmol_per_kilogram: Unit
    kmol_kg: Unit
    micromole_per_gram: Unit
    mu_mathrm_mol_mathrm_g: Unit
    millimole_per_gram: Unit
    mmol_g: Unit
    picomole_per_gram: Unit
    pmol_g: Unit
    pound_mole_per_pound: Unit
    mathrm_lb_mathrm_mol_mathrm_lb_or_mole_lb: Unit
    lb_mol_lb: Unit
    mole_lb: Unit

class MolarFlowRateUnits:
    """Unit constants for Molar Flow Rate."""
    __slots__: tuple[()]

    gram_mole_per_day: Unit
    mol_d: Unit
    gram_mole_per_hour: Unit
    mol_h: Unit
    gram_mole_per_minute: Unit
    mol_min: Unit
    gram_mole_per_second: Unit
    mol_s: Unit
    kilogram_mole_or_kmol_per_day: Unit
    kmol_d: Unit
    kilogram_mole_or_kmol_per_hour: Unit
    kmol_h: Unit
    kilogram_mole_or_kmol_per_minute: Unit
    kmol_min: Unit
    kilogram_mole_or_kmol_per_second: Unit
    kmol_s: Unit
    pound_mole_or_lb_mol_per_day: Unit
    lb_mol_d_or_mole_da: Unit
    lb_mol_d: Unit
    mole_da: Unit
    pound_mole_or_lb_mol_per_hour: Unit
    lb_mol_h_or_mole_hr: Unit
    lb_mol_h: Unit
    mole_hr: Unit
    pound_mole_or_lb_mol_per_minute: Unit
    lb_mol_min_or_mole_min: Unit
    lb_mol_min: Unit
    mole_min: Unit
    pound_mole_or_lb_mol_per_second: Unit
    mathrm_lb_mathrm_mol_mathrm_s_or_mole_sec: Unit
    lb_mol_s: Unit
    mole_sec: Unit

class MolarFluxUnits:
    """Unit constants for Molar Flux."""
    __slots__: tuple[()]

    kmol_per_square_meter_per_day: Unit
    mathrm_kmol_left_mathrm_m_2_mathrm_d_right: Unit
    kmol_per_square_meter_per_hour: Unit
    mathrm_kmol_left_mathrm_m_2_mathrm_h_right: Unit
    kmol_per_square_meter_per_minute: Unit
    mathrm_kmol_left_mathrm_m_2_right_amin: Unit
    kmol_per_square_meter_per_second: Unit
    mathrm_kmol_left_mathrm_m_2_mathrm_s_right: Unit
    pound_mole_per_square_foot_per_day: Unit
    mathrm_lb_mathrm_mol_left_mathrm_ft_2_mathrm_d_right_or_mole_sqft_da: Unit
    lb_mol_left_ft_2_dright: Unit
    mole_sqft_da: Unit
    pound_mole_per_square_foot_per_hour: Unit
    mathrm_lb_mathrm_mol_left_mathrm_ft_2_mathrm_h_right_or_mole_sqft_hr: Unit
    lb_mol_left_ft_2_hright: Unit
    mole_sqft_hr: Unit
    pound_mole_per_square_foot_per_minute: Unit
    mathrm_lb_mathrm_mol_left_mathrm_ft_2_mathrm_min_right_or_mole_sqft_min: Unit
    lb_mol_left_ft_2_minright: Unit
    mole_sqft_min: Unit
    pound_mole_per_square_foot_per_second: Unit
    mathrm_lb_mathrm_mol_left_mathrm_ft_2_mathrm_s_right_or_mole_sqft_sec: Unit
    lb_mol_left_ft_2_sright: Unit
    mole_sqft_sec: Unit

class MolarHeatCapacityUnits:
    """Unit constants for Molar Heat Capacity."""
    __slots__: tuple[()]

    btu_per_pound_mole_per_degree_fahrenheit_or_degree_rankine: Unit
    Btu_lb_mol_circ_mathrm_F: Unit
    calories_per_gram_mole_per_kelvin_or_degree_celsius: Unit
    cal_mol_K: Unit
    joule_per_gram_mole_per_kelvin_or_degree_celsius: Unit
    J_mol_K: Unit

class MolarityOfIUnits:
    """Unit constants for Molarity of "i"."""
    __slots__: tuple[()]

    gram_moles_of_i_per_cubic_meter: Unit
    mathrm_mol_mathrm_i_mathrm_m_3_or_mathrm_c_mathrm_i: Unit
    mol_i_m_3: Unit
    c_i: Unit
    gram_moles_of_i_per_liter: Unit
    mathrm_mol_mathrm_i_mathrm_l: Unit
    kilogram_moles_of_i_per_cubic_meter: Unit
    mathrm_kmol_mathrm_i_mathrm_m_3: Unit
    kilogram_moles_of_i_per_liter: Unit
    mathrm_kmol_mathrm_i_mathrm_l: Unit
    pound_moles_of_i_per_cubic_foot: Unit
    lb_mathrm_mol_mathrm_i_mathrm_ft_3_or_mathrm_mole_mathrm_i_cft: Unit
    lb_mol_i_ft_3: Unit
    mole_i_cft: Unit
    pound_moles_of_i_per_gallon_us: Unit
    lb_mathrm_mol_mathrm_i_mathrm_gal_or_mathrm_mole_mathrm_i_gal: Unit
    lb_mol_i_gal: Unit
    mole_i_gal: Unit

class MoleFractionOfIUnits:
    """Unit constants for Mole Fraction of "i"."""
    __slots__: tuple[()]

    gram_mole_of_i_per_gram_mole_total: Unit
    mathrm_mol_mathrm_i_mathrm_mol: Unit
    kilogram_mole_of_i_per_kilogram_mole_total: Unit
    mathrm_kmol_mathrm_i_mathrm_kmol: Unit
    kilomole_of_i_per_kilomole_total: Unit
    pound_mole_of_i_per_pound_mole_total: Unit
    lb_mathrm_mol_mathrm_i_mathrm_lb_mathrm_mol: Unit

class MomentOfInertiaUnits:
    """Unit constants for Moment of Inertia."""
    __slots__: tuple[()]

    gram_force_centimeter_square_second: Unit
    mathrm_g_mathrm_f_mathrm_cm_mathrm_s_2: Unit
    gram_square_centimeter: Unit
    mathrm_g_mathrm_cm_2: Unit
    kilogram_force_centimeter_square_second: Unit
    mathrm_kg_mathrm_f_mathrm_cm_mathrm_s_2: Unit
    kilogram_force_meter_square_second: Unit
    mathrm_kg_mathrm_f_mathrm_m_mathrm_s_2: Unit
    kilogram_square_centimeter: Unit
    mathrm_kg_mathrm_cm_2: Unit
    kilogram_square_meter: Unit
    mathrm_kg_mathrm_m_2: Unit
    ounce_force_inch_square_second: Unit
    mathrm_oz_mathrm_f_in_mathrm_s_2: Unit
    ounce_mass_square_inch: Unit
    oz_in_2: Unit
    pound_mass_square_foot: Unit
    lb_ft_2_or_lb_sq_ft: Unit
    lb_ft_2: Unit
    lb_sq_ft: Unit
    pound_mass_square_inch: Unit
    mathrm_lb_mathrm_in_2: Unit

class MomentumFlowRateUnits:
    """Unit constants for Momentum Flow Rate."""
    __slots__: tuple[()]

    foot_pounds_per_square_hour: Unit
    mathrm_ft_mathrm_lb_mathrm_h_2_or_mathrm_ft_mathrm_lb_mathrm_hr_2: Unit
    ft_lb_h_2: Unit
    ft_lb_hr_2: Unit
    foot_pounds_per_square_minute: Unit
    mathrm_ft_mathrm_lb_mathrm_min_2: Unit
    foot_pounds_per_square_second: Unit
    mathrm_ft_mathrm_lb_mathrm_s_2_or_ft_lb_sec_2: Unit
    ft_lb_s_2: Unit
    ft_lb_sec_2: Unit
    gram_centimeters_per_square_second: Unit
    mathrm_g_mathrm_cm_mathrm_s_2: Unit
    kilogram_meters_per_square_second: Unit
    mathrm_kg_mathrm_m_mathrm_s_2: Unit

class MomentumFluxUnits:
    """Unit constants for Momentum Flux."""
    __slots__: tuple[()]

    dyne_per_square_centimeter: Unit
    dyn_mathrm_cm_2: Unit
    gram_per_centimeter_per_square_second: Unit
    newton_per_square_meter: Unit
    mathrm_N_mathrm_m_2: Unit
    pound_force_per_square_foot: Unit
    mathrm_lb_mathrm_f_mathrm_sq_mathrm_ft: Unit
    pound_mass_per_foot_per_square_second: Unit
    mathrm_lb_mathrm_m_mathrm_ft_mathrm_s_2_or_mathrm_lb_mathrm_ft_mathrm_sec_2: Unit
    lb_m_ft_s_2: Unit
    lb_ft_sec_2: Unit

class NormalityOfSolutionUnits:
    """Unit constants for Normality of Solution."""
    __slots__: tuple[()]

    gram_equivalents_per_cubic_meter: Unit
    mathrm_eq_mathrm_m_3: Unit
    gram_equivalents_per_liter: Unit
    eq_l: Unit
    pound_equivalents_per_cubic_foot: Unit
    mathrm_lb_mathrm_eq_mathrm_ft_3_or_lb_eq_cft: Unit
    lb_eq_ft_3: Unit
    lb_eq_cft: Unit
    pound_equivalents_per_gallon: Unit
    lb_eq_gal_US: Unit

class ParticleDensityUnits:
    """Unit constants for Particle Density."""
    __slots__: tuple[()]

    particles_per_cubic_centimeter: Unit
    part_cm_3_or_part_cc: Unit
    part_cm_3: Unit
    part_cc: Unit
    particles_per_cubic_foot: Unit
    part_mathrm_ft_3_or_part_cft: Unit
    part_ft_3: Unit
    part_cft: Unit
    particles_per_cubic_meter: Unit
    part_mathrm_m_3: Unit
    particles_per_gallon_us: Unit
    part_gal: Unit
    particles_per_liter: Unit
    part_l: Unit
    particles_per_milliliter: Unit
    part_ml: Unit

class PercentUnits:
    """Unit constants for Percent."""
    __slots__: tuple[()]

    percent: Unit
    per_mille: Unit
    basis_point: Unit
    bp: Unit
    bps: Unit

class PermeabilityUnits:
    """Unit constants for Permeability."""
    __slots__: tuple[()]

    darcy: Unit
    square_feet: Unit
    mathrm_ft_2_or_sq_ft: Unit
    square_meters: Unit

class PhotonEmissionRateUnits:
    """Unit constants for Photon Emission Rate."""
    __slots__: tuple[()]

    rayleigh: Unit
    R: Unit
    reciprocal_square_meter_second: Unit

class PowerPerUnitMassUnits:
    """Unit constants for Power per Unit Mass or Specific Power."""
    __slots__: tuple[()]

    british_thermal_unit_per_hour_per_pound_mass: Unit
    Btu_h_lb_or_Btu_lb_hr: Unit
    Btu_h_lb: Unit
    Btu_lb_hr: Unit
    calorie_per_second_per_gram: Unit
    cal_s_g_or_cal_g_sec: Unit
    cal_s_g: Unit
    cal_g_sec: Unit
    kilocalorie_per_hour_per_kilogram: Unit
    kcal_h_kg_or_kcal_kg_hr: Unit
    kcal_h_kg: Unit
    kcal_kg_hr: Unit
    watt_per_kilogram: Unit
    W_kg: Unit

class PowerPerUnitVolumeUnits:
    """Unit constants for Power per Unit Volume or Power Density."""
    __slots__: tuple[()]

    british_thermal_unit_per_hour_per_cubic_foot: Unit
    mathrm_Btu_mathrm_h_mathrm_ft_3_or_mathrm_Btu_mathrm_hr_cft: Unit
    Btu_h_ft_3: Unit
    Btu_hr_cft: Unit
    calorie_per_second_per_cubic_centimeter: Unit
    mathrm_cal_mathrm_s_mathrm_cm_3_or_mathrm_cal_mathrm_s_mathrm_cc: Unit
    cal_s_cm_3: Unit
    cal_s_cc: Unit
    chu_per_hour_per_cubic_foot: Unit
    Chu_h_ft3_or_Chu_hr_cft: Unit
    Chu_h_ft3: Unit
    Chu_hr_cft: Unit
    kilocalorie_per_hour_per_cubic_centimeter: Unit
    mathrm_kcal_mathrm_h_mathrm_cm_3_or_mathrm_kcal_hr_cc: Unit
    kcal_h_cm_3: Unit
    kcal_hr_cc: Unit
    kilocalorie_per_hour_per_cubic_foot: Unit
    mathrm_kcal_mathrm_h_mathrm_ft_3_or_mathrm_kcal_mathrm_hr_cft: Unit
    kcal_h_ft_3: Unit
    kcal_hr_cft: Unit
    kilocalorie_per_second_per_cubic_centimeter: Unit
    kcal_s_cm_3_or_kcal_s_cc: Unit
    kcal_s_cm_3: Unit
    kcal_s_cc: Unit
    watt_per_cubic_meter: Unit
    mathrm_W_mathrm_m_3: Unit

class PowerThermalDutyUnits:
    """Unit constants for Power, Thermal Duty."""
    __slots__: tuple[()]

    abwatt_emu_of_power: Unit
    emu: Unit
    boiler_horsepower: Unit
    HP_boiler: Unit
    british_thermal_unit_mean: Unit
    british_thermal_unit_mean: Unit
    british_thermal_unit_thermochemical: Unit
    british_thermal_unit_thermochemical: Unit
    calorie_mean: Unit
    calorie_thermochemical: Unit
    donkey: Unit
    erg_per_second: Unit
    erg_s: Unit
    foot_pondal_per_second: Unit
    ft_pdl_s: Unit
    foot_pound_force_per_hour: Unit
    mathrm_ft_mathrm_lb_mathrm_f_mathrm_hr: Unit
    foot_pound_force_per_minute: Unit
    mathrm_ft_mathrm_lb_mathrm_f_min: Unit
    foot_pound_force_per_second: Unit
    mathrm_ft_mathrm_lb_mathrm_f_mathrm_s: Unit
    horsepower_550_mathrmft_mathrmlb_mathrmf_mathrms: Unit
    HP: Unit
    horsepower_electric: Unit
    HP_elect: Unit
    horsepower_uk: Unit
    HP_UK: Unit
    kcal_per_hour: Unit
    kcal_hr: Unit
    kilogram_force_meter_per_second: Unit
    mathrm_kg_mathrm_f_mathrm_m_mathrm_s: Unit
    kilowatt: Unit
    kW: Unit
    megawatt: Unit
    MW: Unit
    metric_horsepower: Unit
    HP_metric: Unit
    million_british_thermal_units_per_hour_petroleum: Unit
    MMBtu_hr: Unit
    million_kilocalorie_per_hour: Unit
    MM_kcal_hr: Unit
    prony: Unit
    ton_of_refrigeration_us: Unit
    CTR_US: Unit
    ton_or_refrigeration_uk: Unit
    CTR_UK: Unit
    volt_ampere: Unit
    VA: Unit
    water_horsepower: Unit
    HP_water: Unit
    watt: Unit
    W: Unit
    watt_international_mean: Unit
    W_int_mean: Unit
    watt_international_us: Unit
    watt_int_US: Unit

class PressureUnits:
    """Unit constants for Pressure."""
    __slots__: tuple[()]

    atmosphere_standard: Unit
    atm: Unit
    bar: Unit
    barye: Unit
    dyne_per_square_centimeter: Unit
    foot_of_mercury_60_circ_mathrmf: Unit
    ft_Hg_60_circ_mathrm_F: Unit
    foot_of_water_60_circ_mathrmf: Unit
    ft_mathrm_H_2_mathrm_O_left_60_circ_mathrm_F_right: Unit
    gigapascal: Unit
    GPa: Unit
    hectopascal: Unit
    hPa: Unit
    inch_of_mercury_60_circ_mathrmf: Unit
    in_mathrm_Hg_left_60_circ_mathrm_F_right: Unit
    inch_of_water_60_circ_mathrmf: Unit
    in_mathrm_H_2_mathrm_O_left_60_circ_mathrm_F_right: Unit
    kilogram_force_per_square_centimeter: Unit
    at_or_mathrm_kg_mathrm_f_mathrm_cm_2: Unit
    at: Unit
    kg_f_cm_2: Unit
    kilogram_force_per_square_meter: Unit
    mathrm_kg_mathrm_f_mathrm_m_2: Unit
    kip_force_per_square_inch: Unit
    KSI_or_ksi_or_kip_f_mathrm_in_2: Unit
    KSI: Unit
    ksi: Unit
    kip_f_in_2: Unit
    megapascal: Unit
    MPa: Unit
    meter_of_water_4circ_mathrmc: Unit
    mathrm_m_mathrm_H_2_mathrm_O_left_4_circ_mathrm_C_right: Unit
    microbar: Unit
    mu_mathrm_bar: Unit
    millibar: Unit
    mbar: Unit
    millimeter_of_mercury_4circ_mathrmc: Unit
    mathrm_mm_mathrm_Hg_left_4_circ_mathrm_C_right: Unit
    millimeter_of_water_4circ_mathrmc: Unit
    mathrm_mm_mathrm_H_2_mathrm_O_left_4_circ_mathrm_C_right: Unit
    newton_per_square_meter: Unit
    ounce_force_per_square_inch: Unit
    OSI_or_osi_or_mathrm_oz_mathrm_f_mathrm_in_2: Unit
    OSI: Unit
    osi: Unit
    pascal: Unit
    Pa: Unit
    pi_ze: Unit
    pz: Unit
    pound_force_per_square_foot: Unit
    pound_force_per_square_inch: Unit
    psi: Unit
    torr: Unit
    torr_or_mm_Hg_0_circ_C: Unit
    mm_Hg_0_circ_C: Unit

class RadiationDoseEquivalentUnits:
    """Unit constants for Radiation Dose Equivalent."""
    __slots__: tuple[()]

    rem: Unit
    sievert: Unit
    Sv: Unit

class RadiationExposureUnits:
    """Unit constants for Radiation Exposure."""
    __slots__: tuple[()]

    coulomb_per_kilogram: Unit
    C_kg: Unit
    d_unit: Unit
    D_unit: Unit
    pastille_dose_b_unit: Unit
    B_unit: Unit
    r_entgen: Unit

class RadioactivityUnits:
    """Unit constants for Radioactivity."""
    __slots__: tuple[()]

    becquerel: Unit
    Bq: Unit
    curie: Unit
    Ci: Unit
    mache_unit: Unit
    Mache: Unit
    rutherford: Unit
    Rd: Unit
    stat: Unit

class SecondMomentOfAreaUnits:
    """Unit constants for Second Moment of Area."""
    __slots__: tuple[()]

    inch_quadrupled: Unit
    in_4: Unit
    centimeter_quadrupled: Unit
    mathrm_cm_4: Unit
    foot_quadrupled: Unit
    mathrm_ft_4: Unit
    meter_quadrupled: Unit
    mathrm_m_4: Unit

class SecondRadiationConstantPlanckUnits:
    """Unit constants for Second Radiation Constant (Planck)."""
    __slots__: tuple[()]

    meter_kelvin: Unit
    m_K: Unit

class SpecificEnthalpyUnits:
    """Unit constants for Specific Enthalpy."""
    __slots__: tuple[()]

    british_thermal_unit_mean: Unit
    british_thermal_unit_per_pound: Unit
    calorie_per_gram: Unit
    chu_per_pound: Unit
    joule_per_kilogram: Unit
    kilojoule_per_kilogram: Unit
    kJ_kg: Unit

class SpecificGravityUnits:
    """Unit constants for Specific Gravity."""
    __slots__: tuple[()]

    dimensionless: Unit

class SpecificHeatCapacityConstantPressureUnits:
    """Unit constants for Specific Heat Capacity (Constant Pressure)."""
    __slots__: tuple[()]

    btu_per_pound_per_degree_fahrenheit_or_degree_rankine: Unit
    Btu_lb_circ_mathrm_F: Unit
    calories_per_gram_per_kelvin_or_degree_celsius: Unit
    cal_g_K: Unit
    joules_per_kilogram_per_kelvin_or_degree_celsius: Unit
    J_kg_K: Unit

class SpecificLengthUnits:
    """Unit constants for Specific Length."""
    __slots__: tuple[()]

    centimeter_per_gram: Unit
    cm_g: Unit
    cotton_count: Unit
    ft_per_pound: Unit
    ft_lb: Unit
    meters_per_kilogram: Unit
    m_kg: Unit
    newton_meter: Unit
    Nm: Unit
    worsted: Unit

class SpecificSurfaceUnits:
    """Unit constants for Specific Surface."""
    __slots__: tuple[()]

    square_centimeter_per_gram: Unit
    mathrm_cm_2_mathrm_g: Unit
    square_foot_per_kilogram: Unit
    mathrm_ft_2_mathrm_kg_or_sq_ft_kg: Unit
    ft_2_kg: Unit
    sq_ft_kg: Unit
    square_foot_per_pound: Unit
    mathrm_ft_2_mathrm_lb_or_sq_ft_lb: Unit
    ft_2_lb: Unit
    sq_ft_lb: Unit
    square_meter_per_gram: Unit
    mathrm_m_2_mathrm_g: Unit
    square_meter_per_kilogram: Unit
    mathrm_m_2_mathrm_kg: Unit

class SpecificVolumeUnits:
    """Unit constants for Specific Volume."""
    __slots__: tuple[()]

    cubic_centimeter_per_gram: Unit
    mathrm_cm_3_mathrm_g_or_mathrm_cc_mathrm_g: Unit
    cm_3_g: Unit
    cc_g: Unit
    cubic_foot_per_kilogram: Unit
    mathrm_ft_3_mathrm_kg_or_mathrm_cft_mathrm_kg: Unit
    ft_3_kg: Unit
    cft_kg: Unit
    cubic_foot_per_pound: Unit
    mathrm_ft_3_mathrm_lb_or_mathrm_cft_mathrm_lb: Unit
    ft_3_lb: Unit
    cft_lb: Unit
    cubic_meter_per_kilogram: Unit
    mathrm_m_3_mathrm_kg: Unit

class StressUnits:
    """Unit constants for Stress."""
    __slots__: tuple[()]

    dyne_per_square_centimeter: Unit
    gigapascal: Unit
    hectopascal: Unit
    kilogram_force_per_square_centimeter: Unit
    kilogram_force_per_square_meter: Unit
    kip_force_per_square_inch: Unit
    megapascal: Unit
    newton_per_square_meter: Unit
    ounce_force_per_square_inch: Unit
    pascal: Unit
    pound_force_per_square_foot: Unit
    pound_force_per_square_inch: Unit

class SurfaceMassDensityUnits:
    """Unit constants for Surface Mass Density."""
    __slots__: tuple[()]

    gram_per_square_centimeter: Unit
    gram_per_square_meter: Unit
    mathrm_g_mathrm_m_2: Unit
    kilogram_per_square_meter: Unit
    pound_mass: Unit
    pound_mass: Unit

class SurfaceTensionUnits:
    """Unit constants for Surface Tension."""
    __slots__: tuple[()]

    dyne_per_centimeter: Unit
    dyn_cm: Unit
    gram_force_per_centimeter: Unit
    mathrm_g_mathrm_f_mathrm_cm: Unit
    newton_per_meter: Unit
    N_m: Unit
    pound_force_per_foot: Unit
    mathrm_lb_mathrm_f_mathrm_ft: Unit
    pound_force_per_inch: Unit
    mathrm_lb_mathrm_f_mathrm_in: Unit

class TemperatureUnits:
    """Unit constants for Temperature."""
    __slots__: tuple[()]

    degree_celsius_unit_size: Unit
    mathrm_C_circ: Unit
    degree_fahrenheit_unit_size: Unit
    mathrm_F_circ: Unit
    degree_r_aumur_unit_size: Unit
    R_circ: Unit
    kelvin_absolute_scale: Unit
    K: Unit
    rankine_absolute_scale: Unit
    circ_mathrm_R: Unit

class ThermalConductivityUnits:
    """Unit constants for Thermal Conductivity."""
    __slots__: tuple[()]

    btu_it: Unit
    Btu_IT_in_hr_circ_mathrm_F: Unit
    btu_therm: Unit
    mathrm_Btu_left_mathrm_ft_mathrm_hr_circ_mathrm_F_right: Unit
    btu_therm: Unit
    calorie_therm: Unit
    operatorname_cal_mathrm_IT_left_mathrm_cm_mathrm_s_circ_mathrm_C_right: Unit
    joule_per_second_per_centimeter_per_kelvin: Unit
    J_cm_s_K: Unit
    watt_per_centimeter_per_kelvin: Unit
    W_cm_K: Unit
    watt_per_meter_per_kelvin: Unit
    W_m_K: Unit

class TimeUnits:
    """Unit constants for Time."""
    __slots__: tuple[()]

    blink: Unit
    century: Unit
    chronon_or_tempon: Unit
    gigan_or_eon: Unit
    Ga_or_eon: Unit
    Ga: Unit
    eon: Unit
    hour: Unit
    h_or_hr: Unit
    h: Unit
    hr: Unit
    julian_year: Unit
    a_jul_or_yr: Unit
    a_jul: Unit
    yr: Unit
    mean_solar_day: Unit
    da_or_d: Unit
    da: Unit
    d: Unit
    millenium: Unit
    minute: Unit
    min: Unit
    second: Unit
    s: Unit
    shake: Unit
    sidereal_year_1900_ad: Unit
    a_sider_or_yr: Unit
    a_sider: Unit
    tropical_year: Unit
    a_trop: Unit
    wink: Unit
    year: Unit
    a_or_y_or_yr: Unit
    y: Unit

class TorqueUnits:
    """Unit constants for Torque."""
    __slots__: tuple[()]

    centimeter_kilogram_force: Unit
    cm_kg_mathrm_f: Unit
    dyne_centimeter: Unit
    foot_kilogram_force: Unit
    mathrm_ft_mathrm_kg_mathrm_f: Unit
    foot_pound_force: Unit
    mathrm_ft_mathrm_lb_mathrm_f: Unit
    foot_poundal: Unit
    in_pound_force: Unit
    in_mathrm_lb_mathrm_f: Unit
    inch_ounce_force: Unit
    in_mathrm_OZ_mathrm_f: Unit
    meter_kilogram_force: Unit
    mathrm_m_mathrm_kg_mathrm_f: Unit
    newton_centimeter: Unit
    N_cm: Unit
    newton_meter: Unit

class TurbulenceEnergyDissipationRateUnits:
    """Unit constants for Turbulence Energy Dissipation Rate."""
    __slots__: tuple[()]

    square_foot_per_cubic_second: Unit
    mathrm_ft_2_mathrm_s_3_or_sq_ft_sec_3: Unit
    ft_2_s_3: Unit
    sq_ft_sec_3: Unit
    square_meter_per_cubic_second: Unit
    mathrm_m_2_mathrm_s_3: Unit

class VelocityAngularUnits:
    """Unit constants for Velocity, Angular."""
    __slots__: tuple[()]

    degree_per_minute: Unit
    deg_min_or_circ_mathrm_min: Unit
    deg_min: Unit
    circ_min: Unit
    degree_per_second: Unit
    deg_s_or_circ_s: Unit
    deg_s: Unit
    circ_s: Unit
    grade_per_minute: Unit
    gon_min_or_grad_min: Unit
    gon_min: Unit
    grad_min: Unit
    radian_per_minute: Unit
    mathrm_rad_mathrm_min: Unit
    radian_per_second: Unit
    mathrm_rad_mathrm_s: Unit
    revolution_per_minute: Unit
    rev_m_or_rpm: Unit
    rev_m: Unit
    rpm: Unit
    revolution_per_second: Unit
    rev_s_or_rps: Unit
    rev_s: Unit
    rps: Unit
    turn_per_minute: Unit
    tr_min: Unit

class VelocityLinearUnits:
    """Unit constants for Velocity, Linear."""
    __slots__: tuple[()]

    foot_per_hour: Unit
    ft_h_or_ft_hr_or_fph: Unit
    ft_h: Unit
    ft_hr: Unit
    fph: Unit
    foot_per_minute: Unit
    ft_min_or_fpm: Unit
    ft_min: Unit
    fpm: Unit
    foot_per_second: Unit
    ft_s_or_fps: Unit
    ft_s: Unit
    fps: Unit
    inch_per_second: Unit
    in_s_or_ips: Unit
    in_s: Unit
    ips: Unit
    international_knot: Unit
    knot: Unit
    kilometer_per_hour: Unit
    km_h_ot_kph: Unit
    kilometer_per_second: Unit
    km_s: Unit
    meter_per_second: Unit
    mathrm_m_mathrm_s: Unit
    mile_per_hour: Unit
    mathrm_mi_mathrm_h_or_mathrm_mi_mathrm_hr_or_mph: Unit
    mi_h: Unit
    mi_hr: Unit
    mph: Unit

class ViscosityDynamicUnits:
    """Unit constants for Viscosity, Dynamic."""
    __slots__: tuple[()]

    centipoise: Unit
    cP_or_cPo: Unit
    cP: Unit
    cPo: Unit
    dyne_second_per_square_centimeter: Unit
    dyn_s_mathrm_cm_2: Unit
    kilopound_second_per_square_meter: Unit
    kip_mathrm_s_mathrm_m_2: Unit
    millipoise: Unit
    mP_or_mPo: Unit
    mP: Unit
    mPo: Unit
    newton_second_per_square_meter: Unit
    mathrm_N_mathrm_s_mathrm_m_2: Unit
    pascal_second: Unit
    Pa_s_or_PI: Unit
    Pa_s: Unit
    PI: Unit
    poise: Unit
    P_or_Po: Unit
    P: Unit
    Po: Unit
    pound_force_hour_per_square_foot: Unit
    mathrm_lb_mathrm_f_mathrm_h_mathrm_ft_2_or_mathrm_lb_mathrm_hr_mathrm_sq_ft: Unit
    lb_f_h_ft_2: Unit
    lb_hr_sq_ft: Unit
    pound_force_second_per_square_foot: Unit
    mathrm_lb_mathrm_f_mathrm_s_mathrm_ft_2_or_mathrm_lb_mathrm_sec_mathrm_sq_ft: Unit
    lb_f_s_ft_2: Unit
    lb_sec_sq_ft: Unit

class ViscosityKinematicUnits:
    """Unit constants for Viscosity, Kinematic."""
    __slots__: tuple[()]

    centistokes: Unit
    cSt: Unit
    millistokes: Unit
    mSt: Unit
    square_centimeter_per_second: Unit
    mathrm_cm_2_mathrm_s: Unit
    square_foot_per_hour: Unit
    mathrm_ft_2_mathrm_h_or_mathrm_ft_2_mathrm_hr: Unit
    ft_2_h: Unit
    ft_2_hr: Unit
    square_foot_per_second: Unit
    mathrm_ft_2_mathrm_s: Unit
    square_meters_per_second: Unit
    mathrm_m_2_mathrm_s: Unit
    stokes: Unit
    St: Unit

class VolumeUnits:
    """Unit constants for Volume."""
    __slots__: tuple[()]

    acre_foot: Unit
    ac_ft: Unit
    acre_inch: Unit
    ac_in: Unit
    barrel_us_liquid: Unit
    bbl_US_liq: Unit
    barrel_us_petro: Unit
    bbl: Unit
    board_foot_measure: Unit
    BM_or_fbm: Unit
    BM: Unit
    fbm: Unit
    bushel_us_dry: Unit
    bu_US_dry: Unit
    centiliter: Unit
    cl_or_cL: Unit
    cL: Unit
    cord: Unit
    cord_or_cd: Unit
    cord_foot: Unit
    cord_ft: Unit
    cubic_centimeter: Unit
    mathrm_cm_3_or_cc: Unit
    cm_3: Unit
    cubic_decameter: Unit
    dam_3: Unit
    cubic_decimeter: Unit
    mathrm_dm_3: Unit
    cubic_foot: Unit
    cu_ft_or_ft_3: Unit
    cu_ft: Unit
    ft_3: Unit
    cubic_inch: Unit
    cu_in_or_mathrm_in_3: Unit
    cu_in: Unit
    in_3: Unit
    cubic_kilometer: Unit
    mathrm_km_3: Unit
    cubic_meter: Unit
    mathrm_m_3: Unit
    cubic_micrometer: Unit
    mu_mathrm_m_3: Unit
    cubic_mile_us_intl: Unit
    cu_mi: Unit
    cubic_millimeter: Unit
    mathrm_mm_3: Unit
    cubic_yard: Unit
    cu_yd_or_mathrm_yd_3: Unit
    cu_yd: Unit
    yd_3: Unit
    decast_re: Unit
    dast: Unit
    deciliter: Unit
    dl_or_dL: Unit
    dl: Unit
    dL: Unit
    fluid_drachm_uk: Unit
    fl_dr_UK: Unit
    fluid_dram_us: Unit
    fl_dr_US_liq: Unit
    fluid_ounce_us: Unit
    fl_oz: Unit
    gallon_imperial_uk: Unit
    gal_UK_or_Imp_gal: Unit
    gal_UK: Unit
    Imp_gal: Unit
    gallon_us_dry: Unit
    gal_US_dry: Unit
    gallon_us_liquid: Unit
    gal: Unit
    last: Unit
    liter: Unit
    unit_1_or_L: Unit
    unit_1: Unit
    microliter: Unit
    mu_mathrm_l_or_mu_mathrm_L: Unit
    mu_l: Unit
    mu_L: Unit
    milliliter: Unit
    ml: Unit
    mohr_centicube: Unit
    pint_uk: Unit
    pt_UK: Unit
    pint_us_dry: Unit
    pt_US_dry: Unit
    pint_us_liquid: Unit
    pt: Unit
    quart_us_dry: Unit
    qt_US_dry: Unit
    st_re: Unit
    tablespoon_metric: Unit
    tbsp_Metric: Unit
    tablespoon_us: Unit
    tbsp: Unit
    teaspoon_us: Unit
    tsp: Unit

class VolumeFractionOfIUnits:
    """Unit constants for Volume Fraction of "i"."""
    __slots__: tuple[()]

    cubic_centimeters_of_i_per_cubic_meter_total: Unit
    mathrm_cm_mathrm_i_3_mathrm_m_3_or_mathrm_cc_mathrm_i_mathrm_m_3: Unit
    cm_i_3_m_3: Unit
    cc_i_m_3: Unit
    cubic_foot_of_i_per_cubic_foot_total: Unit
    mathrm_ft_mathrm_i_3_mathrm_ft_3_or_mathrm_cft_mathrm_i_mathrm_cft: Unit
    ft_i_3_ft_3: Unit
    cft_i_cft: Unit
    cubic_meters_of_i_per_cubic_meter_total: Unit
    mathrm_m_mathrm_i_3_mathrm_m_3: Unit
    gallons_of_i_per_gallon_total: Unit
    mathrm_gal_mathrm_i_mathrm_gal: Unit

class VolumetricCalorificHeatingValueUnits:
    """Unit constants for Volumetric Calorific (Heating) Value."""
    __slots__: tuple[()]

    british_thermal_unit_per_cubic_foot: Unit
    mathrm_Btu_mathrm_ft_3_or_Btu_cft: Unit
    Btu_ft_3: Unit
    Btu_cft: Unit
    british_thermal_unit_per_gallon_uk: Unit
    Btu_gal_UK: Unit
    british_thermal_unit_per_gallon_us: Unit
    Btu_gal_US: Unit
    calorie_per_cubic_centimeter: Unit
    mathrm_cal_mathrm_cm_3_or_mathrm_cal_mathrm_cc: Unit
    cal_cm_3: Unit
    cal_cc: Unit
    chu_per_cubic_foot: Unit
    mathrm_Chu_mathrm_ft_3_or_mathrm_Chu_mathrm_cft: Unit
    Chu_ft_3: Unit
    Chu_cft: Unit
    joule_per_cubic_meter: Unit
    mathrm_J_mathrm_m_3: Unit
    kilocalorie_per_cubic_foot: Unit
    mathrm_kcal_mathrm_ft_3_or_mathrm_kcal_mathrm_cft: Unit
    kcal_ft_3: Unit
    kcal_cft: Unit
    kilocalorie_per_cubic_meter: Unit
    mathrm_kcal_mathrm_m_3: Unit
    therm_100_k_btu: Unit
    thm_cft: Unit

class VolumetricCoefficientOfExpansionUnits:
    """Unit constants for Volumetric Coefficient of Expansion."""
    __slots__: tuple[()]

    gram_per_cubic_centimeter_per_kelvin_or_degree_celsius: Unit
    mathrm_g_mathrm_cm_3_mathrm_K_or_g_cc_circ_mathrm_C: Unit
    g_cm_3_K: Unit
    g_cc_circ_C: Unit
    kilogram_per_cubic_meter_per_kelvin_or_degree_celsius: Unit
    mathrm_kg_mathrm_m_3_mathrm_K_or_mathrm_kg_mathrm_m_3_circ_C: Unit
    kg_m_3_K: Unit
    kg_m_3_circ_C: Unit
    pound_per_cubic_foot_per_degree_fahrenheit_or_degree_rankine: Unit
    mathrm_lb_mathrm_ft_3_circ_mathrm_R_or_mathrm_lb_mathrm_cft_circ_mathrm_F: Unit
    lb_ft_3_circ_R: Unit
    lb_cft_circ_F: Unit
    pound_per_cubic_foot_per_kelvin_or_degree_celsius: Unit
    mathrm_lb_mathrm_ft_3_mathrm_K_or_mathrm_lb_mathrm_cft_circ_mathrm_C: Unit
    lb_ft_3_K: Unit
    lb_cft_circ_C: Unit

class VolumetricFlowRateUnits:
    """Unit constants for Volumetric Flow Rate."""
    __slots__: tuple[()]

    cubic_feet_per_day: Unit
    mathrm_ft_3_mathrm_d_or_mathrm_cft_mathrm_da_or_cfd: Unit
    ft_3_d: Unit
    cft_da: Unit
    cfd: Unit
    cubic_feet_per_hour: Unit
    mathrm_ft_3_mathrm_h_or_mathrm_cft_mathrm_hr_or_cfh: Unit
    ft_3_h: Unit
    cft_hr: Unit
    cfh: Unit
    cubic_feet_per_minute: Unit
    mathrm_ft_3_mathrm_min_or_mathrm_cft_mathrm_min_or_cfm: Unit
    ft_3_min: Unit
    cft_min: Unit
    cfm: Unit
    cubic_feet_per_second: Unit
    mathrm_ft_3_mathrm_s_or_cft_sec_or_cfs: Unit
    ft_3_s: Unit
    cft_sec: Unit
    cfs: Unit
    cubic_meters_per_day: Unit
    mathrm_m_3_mathrm_d: Unit
    cubic_meters_per_hour: Unit
    mathrm_m_3_mathrm_h: Unit
    cubic_meters_per_minute: Unit
    mathrm_m_3_min: Unit
    cubic_meters_per_second: Unit
    mathrm_m_3_mathrm_s: Unit
    gallons_per_day: Unit
    gal_d_or_gpd_or_gal_da: Unit
    gal_d: Unit
    gpd: Unit
    gal_da: Unit
    gallons_per_hour: Unit
    gal_h_or_gph_or_gal_hr: Unit
    gal_h: Unit
    gph: Unit
    gal_hr: Unit
    gallons_per_minute: Unit
    gal_min_or_gpm: Unit
    gal_min: Unit
    gpm: Unit
    gallons_per_second: Unit
    gal_s_or_gps_or_gal_sec: Unit
    gal_s: Unit
    gps: Unit
    gal_sec: Unit
    liters_per_day: Unit
    unit_1_d: Unit
    liters_per_hour: Unit
    unit_1_h: Unit
    liters_per_minute: Unit
    liters_per_second: Unit
    unit_1_s: Unit

class VolumetricFluxUnits:
    """Unit constants for Volumetric Flux."""
    __slots__: tuple[()]

    cubic_feet_per_square_foot_per_day: Unit
    mathrm_ft_3_left_mathrm_ft_2_mathrm_d_right_or_mathrm_cft_mathrm_sqft_da: Unit
    ft_3_left_ft_2_dright: Unit
    cft_sqft_da: Unit
    cubic_feet_per_square_foot_per_hour: Unit
    mathrm_ft_3_left_mathrm_ft_2_mathrm_h_right_or_mathrm_cft_mathrm_sqft_hr: Unit
    ft_3_left_ft_2_hright: Unit
    cft_sqft_hr: Unit
    cubic_feet_per_square_foot_per_minute: Unit
    mathrm_ft_3_left_mathrm_ft_2_min_right_or_mathrm_cft_sqft_min: Unit
    ft_3_left_ft_2_min_right: Unit
    cft_sqft_min: Unit
    cubic_feet_per_square_foot_per_second: Unit
    mathrm_ft_3_left_mathrm_ft_2_mathrm_s_right_or_cft_sqft_sec: Unit
    ft_3_left_ft_2_sright: Unit
    cft_sqft_sec: Unit
    cubic_meters_per_square_meter_per_day: Unit
    mathrm_m_3_left_mathrm_m_2_mathrm_d_right: Unit
    cubic_meters_per_square_meter_per_hour: Unit
    mathrm_m_3_left_mathrm_m_2_mathrm_h_right: Unit
    cubic_meters_per_square_meter_per_minute: Unit
    mathrm_m_3_left_mathrm_m_2_mathrm_min_right: Unit
    cubic_meters_per_square_meter_per_second: Unit
    mathrm_m_3_left_mathrm_m_2_mathrm_s_right: Unit
    gallons_per_square_foot_per_day: Unit
    mathrm_gal_left_mathrm_ft_2_mathrm_d_right_or_gal_sqft_da: Unit
    gal_left_ft_2_dright: Unit
    gal_sqft_da: Unit
    gallons_per_square_foot_per_hour: Unit
    mathrm_gal_left_mathrm_ft_2_mathrm_h_right_or_gal_sqft_hr: Unit
    gal_left_ft_2_hright: Unit
    gal_sqft_hr: Unit
    gallons_per_square_foot_per_minute: Unit
    mathrm_gal_left_mathrm_ft_2_mathrm_min_right_or_gal_sqft_min_or_gpm_sqft: Unit
    gal_left_ft_2_minright: Unit
    gal_sqft_min: Unit
    gpm_sqft: Unit
    gallons_per_square_foot_per_second: Unit
    mathrm_gal_left_mathrm_ft_2_mathrm_s_right_or_gal_mathrm_sqft_mathrm_sec: Unit
    gal_left_ft_2_sright: Unit
    gal_sqft_sec: Unit
    liters_per_square_meter_per_day: Unit
    liters_per_square_meter_per_hour: Unit
    liters_per_square_meter_per_minute: Unit
    liters_per_square_meter_per_second: Unit

class VolumetricMassFlowRateUnits:
    """Unit constants for Volumetric Mass Flow Rate."""
    __slots__: tuple[()]

    gram_per_second_per_cubic_centimeter: Unit
    mathrm_g_left_mathrm_s_mathrm_cm_3_right_or_g_s_cc_or_mathrm_g_mathrm_cc_mathrm_sec: Unit
    g_left_s_cm_3right: Unit
    g_s_cc: Unit
    g_cc_sec: Unit
    kilogram_per_hour_per_cubic_foot: Unit
    kg_h_ft_3_or_kg_hr_cft: Unit
    kg_h_ft_3: Unit
    kg_hr_cft: Unit
    kilogram_per_hour_per_cubic_meter: Unit
    kg_h_m3_or_kg_hr_cu_m: Unit
    kg_h_m3: Unit
    kg_hr_cu_m: Unit
    kilogram_per_second_per_cubic_meter: Unit
    mathrm_kg_left_mathrm_s_mathrm_m_3_right_or_kg_sec_cu_m: Unit
    kg_left_s_m_3right: Unit
    kg_sec_cu_m: Unit
    pound_per_hour_per_cubic_foot: Unit
    mathrm_lb_left_mathrm_h_mathrm_ft_3_right_or_mathrm_lb_mathrm_hr_mathrm_cft_or_PPH_cft: Unit
    lb_left_h_ft_3right: Unit
    lb_hr_cft: Unit
    PPH_cft: Unit
    pound_per_minute_per_cubic_foot: Unit
    lb_min_mathrm_ft_3_or_lb_mathrm_min_mathrm_cft: Unit
    lb_min_ft_3: Unit
    lb_min_cft: Unit
    pound_per_second_per_cubic_foot: Unit
    b_s_ft_3_or_lb_sec_cft: Unit
    b_s_ft_3: Unit
    lb_sec_cft: Unit

class WavenumberUnits:
    """Unit constants for Wavenumber."""
    __slots__: tuple[()]

    diopter: Unit
    kayser: Unit
    reciprocal_meter: Unit
    unit_1_m: Unit

# Global registry
ureg: UnitRegistry

