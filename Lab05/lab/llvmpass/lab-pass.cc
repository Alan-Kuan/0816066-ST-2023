/*
  Ref:
  * https://llvm.org/doxygen/
  * https://llvm.org/docs/GettingStarted.html
  * https://llvm.org/docs/WritingAnLLVMPass.html
  * https://llvm.org/docs/ProgrammersManual.html
 */
#include "lab-pass.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/IRBuilder.h"

using namespace llvm;

char LabPass::ID = 0;

bool LabPass::doInitialization(Module& M) {
    return true;
}

static Constant* getI8StrVal(Module& M, char const* str, Twine const& name) {
    LLVMContext& ctx = M.getContext();

    Constant* strConstant = ConstantDataArray::getString(ctx, str);

    GlobalVariable* gvStr = new GlobalVariable(M, strConstant->getType(), true,
                                               GlobalValue::InternalLinkage, strConstant, name);

    Constant* zero = Constant::getNullValue(Type::getInt32Ty(ctx));
    Constant* indices[] = { zero, zero };
    Constant* strVal = ConstantExpr::getGetElementPtr(Type::getInt8PtrTy(ctx),
                                                      gvStr, indices, true);

    return strVal;
}

static FunctionCallee printfPrototype(Module& M) {
    LLVMContext& ctx = M.getContext();

    FunctionType* printf_type = FunctionType::get(
        Type::getInt32Ty(ctx),
        { Type::getInt8PtrTy(ctx) },
        true);

    FunctionCallee printf_callee = M.getOrInsertFunction("printf", printf_type);

    return printf_callee;
}

bool LabPass::runOnModule(Module& M) {
    errs() << "runOnModule\n";

    LLVMContext& ctx = M.getContext();

    FunctionCallee printf_callee = printfPrototype(M);

    Constant* zero = Constant::getNullValue(Type::getInt32Ty(ctx));
    GlobalVariable* depth = new GlobalVariable(M, zero->getType(), false,
                                               GlobalValue::InternalLinkage, zero, "depth");

    for (auto& F : M) {
        if (F.getName() == "printf") {
            continue;
        }
        errs() << F.getName() << "\n";

        // Entering
        BasicBlock& b_start = F.front();
        Instruction& i_start = b_start.front();
        IRBuilder<> builder(&i_start);

        Constant* format_str = builder.CreateGlobalStringPtr("%*s%s: %p\n", "format_str");
        LoadInst* depth_val = builder.CreateLoad(Type::getInt32Ty(ctx), depth, "depth");
        Constant* empty_str = builder.CreateGlobalStringPtr("", "empty_str");
        Constant* func_name = getI8StrVal(M, F.getName().data(), "func_name");
        Constant* func_addr = ConstantExpr::getBitCast(&F, Type::getInt8PtrTy(ctx));

        builder.CreateCall(printf_callee, { format_str, depth_val, empty_str, func_name, func_addr });

        LoadInst* load1 = builder.CreateLoad(Type::getInt32Ty(ctx), depth, "depth");
        Value* increased_depth = builder.CreateAdd(load1, builder.getInt32(1));
        builder.CreateStore(increased_depth, depth);

        // Exiting
        BasicBlock& b_back = F.back();
        Instruction& i_back = b_back.back();
        IRBuilder<> builder_back(&i_back);

        LoadInst* load2 = builder_back.CreateLoad(Type::getInt32Ty(ctx), depth, "depth");
        Value* decreased_depth = builder_back.CreateSub(load2, builder_back.getInt32(1));
        builder_back.CreateStore(decreased_depth, depth);
    }

    return true;
}

static RegisterPass<LabPass> X("labpass", "Lab Pass", false, false);
