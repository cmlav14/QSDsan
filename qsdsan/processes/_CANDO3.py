# -*- coding: utf-8 -*-
'''
QSDsan: Quantitative Sustainable Design for sanitation and resource recovery systems
This module is developed by:
    Joy Zhang <joycheung1994@gmail.com>
This module is under the University of Illinois/NCSA Open Source License.
Please refer to https://github.com/QSD-Group/QSDsan/blob/main/LICENSE.txt
for license details.
'''

from thermosteam.utils import chemicals_user
from thermosteam import settings
from qsdsan import Component, Components, Processes, _pk, Process   # added `Component` and `Process` to the import
from qsdsan.utils import ospath, data_path, save_pickle, load_pickle

__all__ = ('load_CANDO3_cmps', 'CANDO3')

_path = ospath.join(data_path, 'process_data/_CANDO3.tsv')
_path_cmps = ospath.join(data_path, '_CANDO3_cmps.pckl')
_load_components = settings.get_default_chemicals

############# Components with default notation #############
def _create_CANDO3_cmps(pickle=False):
    cmps = Components.load_default()

    # S_NO3 = cmps.S_NO3.copy('S_NO3')
    # S_NO3.description = 'Nitrate'

    # S_NO2 = cmps.S_NO2.copy('S_NO2')
    # S_NO2.description = 'Nitrite'
    
    # S_NH4 = cmps.S_NH4.copy('S_NH4')
    # S_NH4.description = 'Ammonia Nitrogen'

    # S_O2 = cmps.S_O2.copy('S_O2')
    # S_O2.description = 'Oxygen'

    # This component is not in the default set and needs to be create from scratch
    # S_NO = cmps.S_NO.copy('S_NO')
    # S_NO.description = 'Nitrogen Oxide Nitrogen'
    S_NO = Component.from_chemical('S_NO', chemical='NO', description='Nitric oxide',
                                   measured_as='N',  particle_size='Dissolved gas', 
                                   organic=False, degradability='Undegradable')
 
    # This component is not in the default set and needs to be create from scratch
    # S_N2O = cmps.S_N2O.copy('S_N2O')
    # S_N2O.description = 'Nitrous Oxide Nitrogen'

    S_N2O = Component.from_chemical('S_N2O', chemical='N2O', description='Nitrous oxide',
                                   measured_as='N',  particle_size='Dissolved gas', 
                                   organic=False, degradability='Undegradable')
    # S_N2 = cmps.S_N2.copy('S_N2')
    # S_N2.description = 'Nitrogen'
    
    # S_F = cmps.S_F.copy('S_F')
    # S_F.description = 'Readily Degradable Substrate'

    # S_PO4 = cmps.S_PO4.copy('S_PO4')
    # S_PO4.description = 'Phosphate' 
    
    # S_Ac = cmps.S_Ac.copy('S_Ac')
    # S_Ac.description = 'Acetate'
    
    S_ALK = cmps.S_CO3.copy('S_ALK') 
    S_ALK.description = 'Alkalinity'

    X_PHA = cmps.X_PAO_PHA.copy('X_PHA')
    X_PHA.description = 'polyhydroxyalkanoates'
    
    X_PP = cmps.X_PAO_PP_Hi.copy('X_PP')
    X_PP.description = 'polyphosphate biomass'
    
    X_I = cmps.X_U_Inf.copy('X_I')
    X_I.description = 'Residual Inert Biomass'
    
    X_H = cmps.X_OHO.copy('X_H')
    X_H.description = 'Heterotrophic Biomass'
    
    # X_PAO = cmps.X_PAO.copy('X_PAO')
    # X_PAO.description = 'Phosphate Accumilating Organisms'
    
    X_S = cmps.X_B_Subst.copy('X_S')
    X_S.description = 'Slowly Biodegradable Substrate'


    # add water for the creation of WasteStream objects
    # Basically, if you don't need to make any modification to the component (i.e.,
    # it is exactly the component you need), you can skip the copying part.
    cmps_CANDO3 = Components([cmps.S_NO3, cmps.S_NO2, cmps.S_NH4, cmps.S_O2, 
                              S_NO, S_N2O, cmps.S_N2, cmps.S_F, cmps.S_PO4, 
                              cmps.S_Ac, S_ALK, X_PHA, X_PP, X_I, X_H, 
                              cmps.X_PAO, X_S, cmps.H2O])
    cmps_CANDO3.compile()

    if pickle:
        save_pickle(cmps_CANDO3, _path_cmps)
    return cmps_CANDO3



#_create_asm1_cmps(True)

# _create_CANDO3_cmps(True)


def load_CANDO3_cmps():
    if _pk:
        return load_pickle(_path_cmps)
    else:
        return _create_CANDO3_cmps(pickle=False)



############ Processes in ASM1 #################
# params = ('Y_H', 'Y_A', 'f_P',
#           'mu_H', 'K_S', 'K_O_H', 'K_NO', 'b_H',
#           'mu_A', 'K_NH', 'K_O_A', 'b_A',
#           'eta_g', 'k_a', 'k_h', 'K_X', 'eta_h')

# asm1 = Processes.load_from_file(data_path,
#                                 conserved_for=('COD', 'charge', 'N'),
#                                 parameters=params,
#                                 compile=True)

# ASM1 typical values at 20 degree C
# asm1.set_parameters(
#     Y_A = 0.24,                  # autotrophic yield = 0.24 gCOD/gN
#     Y_H = 0.67,                  # heterotrophic yield = 0.67 gCOD/gCOD
#     f_P = 0.08,                  # fraction of biomass yielding particulate products = 0.08, unitless
#     mu_H = 6,                    # heterotrophic maximum specific growth rate = 6.0 d^(-1)
#     K_S = 20,                    # readily biodegradable substrate half saturation coefficient = 20.0 gCOD/m3
#     K_O_H = 0.2,                 # O2 half saturation coefficient = 0.2 gO2/m3
#     K_NO = 0.5,                  # nitrate half saturation coefficient = 0.5 gN/m3
#     b_H = 0.62,                  # heterotrophic biomass decay rate constant = 0.62 d^(-1)
#     eta_g = 0.8,                 # reduction factor for anoxic growth of heterotrophs = 0.8, unitless
#     eta_h = 0.4,                 # anoxic hydrolysis reduction factor = 0.4, unitless
#     k_h = 3.0,                   # hydrolysis rate constant = 3.0 d^(-1)
#     K_X = 0.03,                  # slowly biodegradable substrate half saturation coefficient for hydrolysis = 0.03 gCOD/gCOD
#     mu_A = 0.8,                  # autotrophic maximum specific growth rate = 0.8 d^(-1)
#     K_NH = 1.0,                  # ammonium (nutrient) half saturation coefficient = 1.0 gN/m3
#     K_O_A = 0.4,                 # O2 half saturation coefficient for autotrophic growth = 0.4 gO2/m3
#     b_A = 0.05,                  # !!! BSM1 value
#     k_a = 0.08                   # ammonification rate constant = 0.08 d^(-1)/(gCOD/m3)
#     )

# ASM1 typical values at 10 degree C
# asm1.set_parameters(
#     Y_A = 0.24,                  # autotrophic yield = 0.24 gCOD/gN
#     Y_H = 0.67,                  # heterotrophic yield = 0.67 gCOD/gCOD
#     f_P = 0.08,                  # fraction of biomass yielding particulate products = 0.08, unitless
#     mu_H = 3,                    # heterotrophic maximum specific growth rate = 3.0 d^(-1)
#     K_S = 20,                    # readily biodegradable substrate half saturation coefficient = 20.0 gCOD/m3
#     K_O_H = 0.2,                 # O2 half saturation coefficient = 0.2 gO2/m3
#     K_NO = 0.5,                  # nitrate half saturation coefficient = 0.5 gN/m3
#     b_H = 0.20,                  # heterotrophic biomass decay rate constant = 0.20 d^(-1)
#     eta_g = 0.8,                 # reduction factor for anoxic growth of heterotrophs = 0.8, unitless
#     eta_h = 0.4,                 # anoxic hydrolysis reduction factor = 0.4, unitless
#     k_h = 1.0,                   # hydrolysis rate constant = 1.0 d^(-1)
#     K_X = 0.01,                  # slowly biodegradable substrate half saturation coefficient for hydrolysis = 0.01 gCOD/gCOD
#     mu_A = 0.3,                  # autotrophic maximum specific growth rate = 0.3 d^(-1)
#     K_NH = 1.0,                  # ammonium (nutrient) half saturation coefficient = 1.0 gN/m3
#     K_O_A = 0.4,                 # O2 half saturation coefficient for autotrophic growth = 0.4 gO2/m3
#     b_A = 0.05,                  # !!! BSM1 value
#     k_a = 0.04                   # ammonification rate constant = 0.04 d^(-1)/(gCOD/m3)
#     )

@chemicals_user
class CANDO3(Processes):
    '''
    Activated Sludge Model No. 1 in original notation. [1]_, [2]_
    Parameters
    ----------
    components: class:`CompiledComponents`, optional
        Components corresponding to each entry in the stoichiometry array,
        defaults to thermosteam.settings.chemicals.
    Y_A : float, optional
        Autotrophic yield, in [g COD/g N]. The default is 0.24.
    Y_H : float, optional
        Heterotrophic yield, in [g COD/g COD]. The default is 0.67.
    f_P : float, optional
        Fraction of biomass yielding particulate products. The default is 0.08.
    i_XB : float, optional
        Nitrogen content of biomass, in [g N/g COD]. The default is 0.08.
    i_XP : float, optional
        Nitrogen content of particulate products arising from biomass decay,
        in [g N/g COD]. The default is 0.06.
    mu_H : float, optional
        Heterotrophic maximum specific growth rate, in [d^(-1)]. The default
        is 4.0.
    K_S : float, optional
        Readily biodegradable substrate half saturation coefficient, in [g COD/m^3].
        The default is 10.0.
    K_O_H : float, optional
        Oxygen half saturation coefficient for heterotrophic growth, in [g O2/m^3].
        The default is 0.2.
    K_NO : float, optional
        Nitrate half saturation coefficient, in [g N/m^3]. The default is 0.5.
    b_H : float, optional
        Heterotrophic biomass decay rate constant, in [d^(-1)]. The default is 0.3.
    eta_g : float, optional
        Reduction factor for anoxic growth of heterotrophs. The default is 0.8.
    eta_h : float, optional
        Reduction factor for anoxic hydrolysis. The default is 0.8.
    k_h : float, optional
        Hydrolysis rate constant, in [d^(-1)]. The default is 3.0.
    K_X : float, optional
        Slowly biodegradable substrate half saturation coefficient for hydrolysis,
        in [g COD/g COD]. The default is 0.1.
    mu_A : float, optional
        Autotrophic maximum specific growth rate, in [d^(-1)]. The default is 0.5.
    K_NH : float, optional
        Ammonium (nutrient) half saturation coefficient, in [g N/m^3]. The default
        is 1.0.
    b_A : float, optional
        Autotrophic biomass decay rate constant, in [d^(-1)]. The default is 0.05.
    K_O_A : float, optional
        Oxygen half saturation coefficient for autotrophic growth, in [g O2/m^3].
        The default is 0.4.
    k_a : float, optional
        Ammonification rate constant, in [m^3/g COD/d]. The default is 0.05.
    path : str, optional
        Alternative file path for the Gujer matrix. The default is None.
    References
    ----------
    .. [1] Henze, M.; Gujer, W.; Mino, T.; Loosdrecht, M. van. Activated Sludge
        Models: ASM1, ASM2, ASM2d and ASM3; IWA task group on mathematical modelling
        for design and operation of biological wastewater treatment, Ed.; IWA
        Publishing: London, 2000.
    .. [2] Rieger, L.; Gillot, S.; Langergraber, G.; Ohtsuki, T.; Shaw, A.; Takács,
        I.; Winkler, S. Guidelines for Using Activated Sludge Models; IWA Publishing:
        London, New York, 2012; Vol. 11.
        https://doi.org/10.2166/9781780401164.
    '''

    _params = ('k_H','k_X','mu_H','b_H','nu_H1','nu_H2','nu_H3','nu_H4','k_OH1','k_OH2',
               'k_OH3','k_OH4','k_OH5','k_S1','k_S2','k_S3','k_S4','k_S5',
               'k_HB_NO3', 'k_HB_NO2', 'k_HB_NO', 'k_HB_N2O', 'k_HB_I1_NO',
               'k_HB_I2_NO','k_HB_I3_NO','Y_PHA','Y_PAO','Y_PO4','f_XI','Y_H','f_1','i_NBM','i_NXS','i_PBM','i_NXI',
               'b_PAO','b_PP','b_PHA','k_PP','q_PHA','k_A','k_ALK','q_PP','k_PS',
               'k_MAX','k_P','k_IPP','k_O2','k_NO3','k_PHA','n_NO3','mu_PAO','k_NH4')

    def __new__(cls, components=None, k_H=0.125, k_X=1, mu_H=0.26,
                b_H=0.017,nu_H1=.28,nu_H2=.16,nu_H3=.35,nu_H4=.35,
                k_OH1=.1, k_OH2=.1, k_OH3=.1, k_OH4=.1, k_OH5=.1,
                k_S1=20,k_S2=20,k_S3=20,k_S4=20,k_S5=40,k_HB_NO3=.2,
                k_HB_NO2=.2,k_HB_NO=.05,k_HB_N2O=.05,k_HB_I1_NO=.5,
                k_HB_I2_NO=.3,k_HB_I3_NO=.075,Y_PHA=.625,Y_PAO=.2,Y_PO4=.3,f_XI=.1,Y_H=.625,i_NXI=.02,
                f_1=.1,i_NBM=.07,i_NXS=.02,i_PBM=.07,
                b_PAO =.2,b_PP=.2,b_PHA=.2,k_PP=.01, 
                q_PHA=3.0,k_A=4.0,k_ALK=0.1,q_PP=1.5,k_PS=0.2,k_MAX=0.34,k_P=.01,
                k_IPP=0.02,k_O2=0.2, k_NO3=0.5,k_PHA=0.01,n_NO3=.6,mu_PAO=1,k_NH4=.05,
                fr_SS_COD=0.75, path=None, **kwargs):
        if not path: path = _path
        
        cmps = _load_components(components)
        cmps.X_I.i_mass  = fr_SS_COD

        cmps.refresh_constants()
        
        # Added 'P' to conserved_for
        self = Processes.load_from_file(path,
                                        conserved_for=('COD', 'charge', 'N', 'P'),
                                        parameters=cls._params,
                                        components=cmps,
                                        compile=False)
        
        if path == _path:
            _p12 = Process('anox_storage_PP',
                           'S_PO4 + [Y_PHA]X_PHA + [?]S_NO3 -> X_PP + [?]S_N2 + [?]S_NH4 + [?]S_ALK',
                           components=cmps,
                           ref_component='X_PP',
                           rate_equation='q_PP * S_O2/(k_O2+S_O2) * S_PO4/(k_PS+S_PO4) * S_ALK/(k_ALK+S_ALK) * (X_PHA/X_PAO)/(k_PHA+X_PHA/X_PAO) * (k_MAX-X_PP/X_PAO)/(k_IPP+k_MAX-X_PP/X_PAO) * X_PAO * n_NO3 * k_O2/S_O2 * S_NO3/(k_NO3+S_NO3)',
                           parameters=('Y_PHA', 'q_PP', 'k_O2', 'k_PS', 'k_ALK', 'k_PHA', 'n_NO3', 'k_IPP', 'k_NO3'),
                           conserved_for=('COD', 'N', 'P', 'NOD', 'charge'))

            _p14 = Process('PAO_anox_growth',
                           '[1/Y_PAO]X_PHA + [?]S_NO3 + [?]S_PO4 -> X_PAO + [?]S_N2 + [?]S_NH4  + [?]S_ALK',
                           components=cmps,
                           ref_component='X_PAO',
                           rate_equation='mu_PAO * S_O2/(k_O2 + S_O2) * S_NH4/(k_NH4 + S_NH4) * S_PO4/(k_P + S_PO4) * S_ALK/(k_ALK + S_ALK) * (X_PHA/X_PAO)/(k_PHA + X_PHA/X_PAO) * X_PAO * n_NO3 * k_O2/S_O2 * S_NO3/(k_NO3 + S_NO3)',
                           parameters=('Y_PAO', 'mu_PAO', 'k_O2', 'k_NH4', 'k_P', 'k_ALK', 'k_PHA', 'n_NO3', 'k_NO3'),
                           conserved_for=('COD', 'N', 'P', 'NOD', 'charge'))
            self.extend([_p12, _p14])

        self.compile()

        self.set_parameters(k_H=k_H,k_X=k_X,mu_H=mu_H,b_H=b_H,nu_H1=nu_H1,nu_H2=nu_H2,
                            nu_H3=nu_H3,nu_H4=nu_H4,k_OH1=k_OH1,k_OH2=k_OH2,k_OH3=k_OH3,
                            k_OH4=k_OH4,k_OH5=k_OH5,k_S1=k_S1,k_S2=k_S2,k_S3=k_S3,k_S4=k_S4,
                            k_S5=k_S5,k_HB_NO3=k_HB_NO3,k_HB_NO2=k_HB_NO2,k_HB_NO=k_HB_NO,
                            k_HB_N2O=k_HB_N2O,k_HB_I1_NO=k_HB_I1_NO,k_HB_I2_NO=k_HB_I2_NO,
                            k_HB_I3_NO=k_HB_I3_NO,Y_PHA=Y_PHA,Y_PAO=Y_PAO,Y_PO4=Y_PO4,f_XI=f_XI,
                            Y_H=Y_H,b_PAO=b_PAO,b_PP=b_PP,b_PHA=b_PHA,k_PP=k_PP,q_PHA=q_PHA,
                            k_A=k_A,k_ALK=k_ALK,q_PP=q_PP,k_PS=k_PS,k_MAX=k_MAX,k_P=k_P,
                            k_IPP=k_IPP,k_O2=k_O2,k_NO3=k_NO3,k_PHA=k_PHA,n_NO3=n_NO3,
                            mu_PAO=mu_PAO,k_NH4=k_NH4,f_1=f_1,i_NBM=i_NBM,i_NXS=i_NXS,i_PBM=i_PBM,i_NXI=i_NXI,
                            **kwargs)
        return self
