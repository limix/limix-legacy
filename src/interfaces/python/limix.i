// Copyright(c) 2014, The LIMIX developers(Christoph Lippert, Paolo Francesco Casale, Oliver Stegle)
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
%module core
%feature("autodoc", "3");
%include exception.i       

%{
#define SWIG_FILE_WITH_INIT
#define SWIG
#include "limix_legacy/types.h"
#include "limix_legacy/covar/covariance.h"
#include "limix_legacy/utils/cache.h"
#include "limix_legacy/covar/linear.h"
#include "limix_legacy/covar/freeform.h"
#include "limix_legacy/covar/se.h"
#include "limix_legacy/covar/combinators.h"	
#include "limix_legacy/likelihood/likelihood.h"
#include "limix_legacy/mean/ADataTerm.h"
#include "limix_legacy/mean/CData.h"
#include "limix_legacy/mean/CLinearMean.h"
#include "limix_legacy/mean/CSumLinear.h"
#include "limix_legacy/mean/CKroneckerMean.h"
#include "limix_legacy/gp/gp_base.h"
#include "limix_legacy/gp/gp_kronecker.h"
#include "limix_legacy/gp/gp_kronSum.h"
#include "limix_legacy/gp/gp_Sum.h"
#include "limix_legacy/gp/gp_opt.h"
#include "limix_legacy/LMM/lmm.h"
#include "limix_legacy/LMM/kronecker_lmm.h"
#include "limix_legacy/modules/CVarianceDecomposition.h"
#include "limix_legacy/io/dataframe.h"
#include "limix_legacy/io/genotype.h"
#include "limix_legacy/LMM_forest/lmm_forest.h"

using namespace limix;
//  removed namespace bindings (12.02.12)
%}

/* Get the numpy typemaps */
%include "numpy.i"
//support for eigen matrix stuff
%include "eigen.i"
//include typemaps
%include "typemaps.i"

#define SWIG_SHARED_PTR_NAMESPACE std
//C11, no tr!
//#define SWIG_SHARED_PTR_SUBNAMESPACE tr1
%include "std_shared_ptr.i"

//removed boost
//%include <boost_shared_ptr.i>

%include "std_vector.i"
%include "std_map.i"
%include "std_string.i"
%include "stdint.i"


%init %{
  import_array();
%}


%exception{
	try {
	$action
	} catch (limix::CLimixException& e) {
	std::string s("LIMIX error: "), s2(e.what());
	s = s + s2;
	SWIG_exception(SWIG_RuntimeError, s.c_str());
	return NULL;
	} catch (...) {
	SWIG_exception(SWIG_RuntimeError,"Unknown exception");
	}
}


// Includ dedicated interface files
/* Note: currently these only contain definitions of shared pointers. We should move these into interface files below as soon as possible
*/
%include "./../types.i"
%include "./../covar.i"
%include "./../lik.i"
%include "./../mean.i"
%include "./../lmm.i"
%include "./../gp.i"
%include "./../modules.i"
%include "./../io.i"

//interface files:
%include "limix_legacy/types.i"
%include "limix_legacy/utils/cache.i"
%include "limix_legacy/covar/covariance.i"
%include "limix_legacy/covar/linear.i"
%include "limix_legacy/covar/freeform.i"
%include "limix_legacy/covar/se.i"
%include "limix_legacy/covar/combinators.i"	
%include "limix_legacy/likelihood/likelihood.i"
%include "limix_legacy/mean/ADataTerm.i"
%include "limix_legacy/mean/CData.i"
%include "limix_legacy/mean/CLinearMean.i"
%include "limix_legacy/mean/CSumLinear.i"
%include "limix_legacy/mean/CKroneckerMean.i"
%include "limix_legacy/gp/gp_base.i"
%include "limix_legacy/gp/gp_kronecker.i"
%include "limix_legacy/gp/gp_kronSum.i"
%include "limix_legacy/gp/gp_Sum.i"
%include "limix_legacy/gp/gp_opt.i"
%include "limix_legacy/LMM/lmm.i"
%include "limix_legacy/LMM/kronecker_lmm.i"
%include "limix_legacy/modules/CVarianceDecomposition.i"
%include "limix_legacy/io/dataframe.i"
%include "limix_legacy/io/genotype.i"
%include "limix_legacy/LMM_forest/lmm_forest.i"
