// Copyright(c) 2014, The LIMIX developers(Christoph Lippert, Paolo Francesco Casale, Oliver Stegle)
//
//Licensed under the Apache License, Version 2.0 (the "License");
//you may not use this file except in compliance with the License.
//You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
//Unless required by applicable law or agreed to in writing, software
//distributed under the License is distributed on an "AS IS" BASIS,
//WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//See the License for the specific language governing permissions and
//limitations under the License.

#include "ADataTerm.h"

namespace limix {
ADataTerm::ADataTerm()
{
}

ADataTerm::ADataTerm(const MatrixXd& Y)
{
	this->Y = Y;
}

ADataTerm::~ADataTerm()
{
}

void ADataTerm::aEvaluate(MatrixXd* outY)
{
	*outY = this->Y;
}

void ADataTerm::aGradY(MatrixXd* outGradY)
{
	*outGradY = MatrixXd::Ones(this->Y.rows(), this->Y.cols());
}

void ADataTerm::aGradParams(MatrixXd* outGradParams, const MatrixXd* KinvY)
{
	*outGradParams = MatrixXd();
}

void ADataTerm::aSumJacobianGradParams(MatrixXd* outSumJacobianGradParams)
{
	*outSumJacobianGradParams = MatrixXd();
}

void ADataTerm::aSumLogJacobian(MatrixXd* outSumJacobianGradParams)
{
	*outSumJacobianGradParams = MatrixXd();
}



} /* namespace limix */
