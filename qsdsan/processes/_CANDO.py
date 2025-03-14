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
from qsdsan import Components, Processes, _pk
from ..utils import ospath, data_path, save_pickle, load_pickle

__all__ = ('load_CANDO_cmps', 'CANDO')

_path = ospath.join(data_path, 'process_data/_CANDO.tsv')
_path_cmps = ospath.join(data_path, '_CANDO_cmps.pckl')
_load_components = settings.get_default_chemicals

############# Components with default notation #############
def _create_CANDO_cmps(pickle=False):
    cmps = Components.load_default()

    S_NO3 = cmps.S_NO3.copy('S_NO3')
    S_NO3.description = 'Nitrate'

    S_NO2 = cmps.S_NO2.copy('S_NO2')
    S_NO2.description = 'Nitrite'

    S_NO = cmps.S_NO.copy('S_NO')
    S_NO.description = 'Nitrogen Oxide Nitrogen'
 
    S_N2O = cmps.S_N2O.copy('S_N2O')
    S_N2O.description = 'Nitrous Oxide Nitrogen'
   
    S_N2 = cmps.S_N2.copy('S_N2')
    S_N2.description = 'Nitrogen'
    
    S_S = cmps.S_F.copy('S_S')
    S_S.description = 'Readily Degradable Substrate'

    S_F = cmps.S_F.copy('S_F')
    S_F.description = 'Readily Degradable Substrate'

    S_PO4 = cmps.S_PO4.copy('S_PO4')
    S_PO4.description = 'Phosphate' 

    X_DPAO = cmps.X_DPAO.copy('X_DPAO')
    X_DPAO.description = 'Denitrifying Phosphorus Accumilating Organismss'
    
    X_PHA = cmps.X_PAO_PHA.copy('X_PHA')
    X_PHA.description = 'polyhydroxyalkanoates'
    
    X_PP = cmps.X_PAO_PP_Hi.copy('X_PP')
    X_PP.description = 'polyphosphate biomass'
    
    X_I = cmps.X_U_Inf.copy('X_I')
    X_I.description = 'Residual Inert Biomass'



    # add water for the creation of WasteStream objects
    cmps_CANDO = Components([S_NO3, S_NO2, S_NO, S_N2O, S_N2, S_F, S_PO4,
                            X_DPAO, X_PHA, X_PP, X_I,
                            cmps.H2O])
    cmps_CANDO.compile()

    if pickle:
        save_pickle(cmps_CANDO, _path_cmps)
    return cmps_CANDO



#_create_CANDO_cmps(True)


def load_CANDO_cmps():
    if _pk:
        return load_pickle(_path_cmps)
    else:
        return _create_CANDO_cmps(pickle=False)



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
class CANDO(Processes):
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

    _params = ('Y_PO4','Y_PHA', 'Y_DPAO_NOx','i_P_BM','i_P_XI', 'f_1','q_PSA','K_S_DPAO',
               'K_PP_DPAO','q_PP','K_PO4_PP','K_PHA','K_max_DPAO','K_iPP_DPAO',
               'K_DPAO_PO4','mu_DPAO1','mu_DPAO2','mu_DPAO3','mu_DPAO4','K_NO3','K_NO2',
               'K_NO2','K_NO','K_N2O','b_DPAO','b_PP','b_PHA','K_NOx')



    def __new__(cls, components=None, Y_PO4=0.3, Y_PHA=0.2, Y_DPAO_NOx=0.5,
                i_P_BM=0.02,
                i_P_XI=0.01,f_1=.2,q_PHA=.53,K_S_DPAO=10,K_PP_DPAO=.05,q_PP=.0375,
                K_PO4_PP=0.2, K_PHA=0.1,K_max_DPAO=0.2,K_iPP_DPAO=.05, 
                K_DPAO_PO4=0.05,mu_DPAO1=0.07, mu_DPAO2=0.019,mu_DPAO3=.142,
                mu_DPAO4=.142,
                K_NO3=.251,K_NO2=.81,K_NO=.0021,K_N2O=.0052,b_DPAO=.005,
                b_PP=.005,b_PHA=.005,K_NOx=.5,
                fr_SS_COD=0.75, path=None, **kwargs):
        if not path: path = _path
        

       
        cmps = _load_components(components)
        cmps.X_I.i_mass  = fr_SS_COD
        cmps.refresh_constants()
        
        self = Processes.load_from_file(path,
                                        conserved_for=('COD', 'charge', 'N'),
                                        parameters=cls._params,
                                        components=cmps,
                                        compile=True)

        self.set_parameters(Y_PO4=Y_PO4,Y_PHA=Y_PHA,Y_DPAO_NOx=Y_DPAO_NOx,
                            i_P_BM=i_P_BM,i_P_XI=i_P_XI,f_1=f_1,q_PHA=q_PHA,
                            K_S_DPAO=K_S_DPAO,K_PP_DPAO=K_PP_DPAO,q_PP=q_PP,
                            K_PO4_PP=K_PO4_PP,K_PHA=K_PHA,K_max_DPAO=K_max_DPAO,
                            K_iPP_DPAO=K_iPP_DPAO,K_DPAO_PO4=K_DPAO_PO4,mu_DPAO1=mu_DPAO1,
                            mu_DPAO2=mu_DPAO2,mu_DPAO3=mu_DPAO3,mu_DPAO4=mu_DPAO4,
                            K_NO3=K_NO3,K_NO2=K_NO2,K_NO=K_NO,K_N2O=K_N2O,
                            b_DPAO=b_DPAO,b_PP=b_PP,b_PHA=b_PHA,K_NOx=K_NOx,
                            **kwargs)
        return self

                            
 
