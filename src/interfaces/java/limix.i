%module core

%{
#define SWIG_FILE_WITH_INIT
#define SWIG
#include "limix_legacy/types.h"
#include "limix_legacy/lasso/lasso.h"
#include "limix_legacy/covar/covariance.h"
#include "limix_legacy/covar/linear.h"
#include "limix_legacy/covar/se.h"
#include "limix_legacy/covar/fixed.h"	
#include "limix_legacy/covar/freeform.h"	
#include "limix_legacy/covar/combinators.h"	
#include "limix_legacy/likelihood/likelihood.h"
#include "limix_legacy/mean/ADataTerm.h"
#include "limix_legacy/mean/CData.h"
#include "limix_legacy/mean/CLinearMean.h"
#include "limix_legacy/mean/CSumLinear.h"
#include "limix_legacy/mean/CKroneckerMean.h"
#include "limix_legacy/gp/gp_base.h"
#include "limix_legacy/gp/gp_kronecker.h"
#include "limix_legacy/gp/gp_opt.h"
#include "limix_legacy/LMM/lmm.h"
#include "limix_legacy/LMM/kronecker_lmm.h"
#include "limix_legacy/LMM/CGPLMM.h"
#include "limix_legacy/modules/CVqtl.h"
#include "limix_legacy/modules/CMultiTraitVQTL.h"


using namespace limix;
//  removed namespace bindings (12.02.12)
%}

/* Get the numpy typemaps */
//%include "numpy.i"
//support for eigen matrix stuff
//%include "eigen.i"
//support for std libs
//suport for std_shared pointers in tr1 namespace

#define SWIG_SHARED_PTR_NAMESPACE std
#define SWIG_SHARED_PTR_SUBNAMESPACE tr1
%include "std_shared_ptr.i"
%include "std_vector.i"
%include "std_map.i"
%include "std_string.i"


%init %{
  import_array();
%}


// Includ dedicated interface files
%include "./../covar.i"
%include "./../gp.i"
%include "./../lik.i"
%include "./../mean.i"
%include "./../lmm.i"
%include "./../modules.i"


//generated outodoc:
//%feature("autodoc", "1")
%include "limix_legacy/types.h"
%include "limix_legacy/lasso/lasso.h"
%include "limix_legacy/covar/covariance.h"
%include "limix_legacy/covar/linear.h"
%include "limix_legacy/covar/se.h"
%include "limix_legacy/covar/fixed.h"
%include "limix_legacy/covar/freeform.h"	
%include "limix_legacy/covar/combinators.h"	
%include "limix_legacy/likelihood/likelihood.h"
%include "limix_legacy/mean/ADataTerm.h"
%include "limix_legacy/mean/CData.h"
%include "limix_legacy/mean/CLinearMean.h"
%include "limix_legacy/mean/CSumLinear.h"
%include "limix_legacy/mean/CKroneckerMean.h"
%include "limix_legacy/gp/gp_base.h"
%include "limix_legacy/gp/gp_kronecker.h"
%include "limix_legacy/gp/gp_opt.h"
%include "limix_legacy/LMM/lmm.h"
%include "limix_legacy/LMM/CGPLMM.h"
%include "limix_legacy/LMM/kronecker_lmm.h"
%include "limix_legacy/modules/CVqtl.h"
%include "limix_legacy/modules/CMultiTraitVQTL.h"



 
