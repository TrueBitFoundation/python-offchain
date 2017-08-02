
/****************************************************Truebit Checker****************************************************/
//-*-c++-*-
/*standard headers*/
/*LLVM headers*/
#include "clang/AST/AST.h"
#include "clang/AST/ASTConsumer.h"
#include "clang/ASTMatchers/ASTMatchers.h"
#include "clang/ASTMatchers/ASTMatchFinder.h"
#include "clang/Frontend/CompilerInstance.h"
#include "clang/Frontend/FrontendActions.h"
#include "clang/Lex/Lexer.h"
#include "clang/Tooling/CommonOptionsParser.h"
#include "clang/Tooling/Tooling.h"
#include "clang/Rewrite/Core/Rewriter.h"
#include "llvm/IR/Function.h"
/**********************************************************************************************************************/
/*used namespaces*/
using namespace llvm;
using namespace clang;
using namespace clang::ast_matchers;
using namespace clang::driver;
using namespace clang::tooling;
/**********************************************************************************************************************/
/*global vars*/
static llvm::cl::OptionCategory TBCCategory("TBC");
/**********************************************************************************************************************/
/*The Matchers go here*/
/**********************************************************************************************************************/
/**********************************************************************************************************************/
class TBCASTConsumer : public ASTConsumer {

public:
  TBCASTConsumer(Rewriter &R){
  }

  void HandleTranslationUnit(ASTContext &Context) override {
    Matcher.matchAST(Context);
  }

private:
  MatchFinder Matcher;
};
/**********************************************************************************************************************/
/**
 * @brief a blank diagnostic consumer
 */
class BlankDiagConsumer : public clang::DiagnosticConsumer
{
  public:
    BlankDiagConsumer() = default;
    virtual ~BlankDiagConsumer() {}
    virtual void HandleDiagnostic(DiagnosticsEngine::Level DiagLevel, const Diagnostic &Info) override {}
};
/**********************************************************************************************************************/
class TBCFrontendAction : public ASTFrontendAction {
public:
  TBCFrontendAction() {}
  ~TBCFrontendAction() {
    delete BDC;
  }
  void EndSourceFileAction() override {
  }

  std::unique_ptr<ASTConsumer> CreateASTConsumer(CompilerInstance &CI, StringRef file) override {
    DiagnosticsEngine &DE = CI.getPreprocessor().getDiagnostics();
    DE.setClient(BDC, false);
    TheRewriter.setSourceMgr(CI.getSourceManager(), CI.getLangOpts());
    return llvm::make_unique<TBCASTConsumer>(TheRewriter);
  }

private:
  BlankDiagConsumer *BDC = new BlankDiagConsumer;
  Rewriter TheRewriter;
};
/**********************************************************************************************************************/
/*Main*/
int main(int argc, const char **argv) {
  CommonOptionsParser op(argc, argv, TBCCategory);
  ClangTool Tool(op.getCompilations(), op.getSourcePathList());

  return Tool.run(newFrontendActionFactory<TBCFrontendAction>().get());
}
/*last line intentionally left blank*/

