/*
  This file is part of the PhantomJS project from Ofi Labs.

  Copyright (C) 2011 Ariya Hidayat <ariya.hidayat@gmail.com>
  Copyright (C) 2011 execjosh, http://execjosh.blogspot.com

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the <organization> nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
  ARE DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
  DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
  (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
  THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

#ifndef CONFIG_H
#define CONFIG_H

#include <QString>
#include <QStringList>

class Config: QObject
{
    Q_OBJECT
    Q_PROPERTY(QString cookieFile READ cookieFile WRITE setCookieFile)
    Q_PROPERTY(bool diskCacheEnabled READ diskCacheEnabled WRITE setDiskCacheEnabled)
    Q_PROPERTY(bool ignoreSslErrors READ ignoreSslErrors WRITE setIgnoreSslErrors)
    Q_PROPERTY(bool localAccessRemote READ localAccessRemote WRITE setLocalAccessRemote)
    Q_PROPERTY(QString outputEncoding READ outputEncoding WRITE setOutputEncoding)
    Q_PROPERTY(bool pluginsEnabled READ pluginsEnabled WRITE setPluginsEnabled)
    Q_PROPERTY(QString proxy READ proxy WRITE setProxy)
    Q_PROPERTY(QString auth READ auth WRITE setAuth)
    Q_PROPERTY(QString scriptEncoding READ scriptEncoding WRITE setScriptEncoding)

public:
    Config(QObject *parent = 0);

    void init(const QStringList *const args);
    void processArgs(const QStringList &args);
    void loadJsonFile(const QString &filePath);

    bool autoLoadImages() const;
    void setAutoLoadImages(const bool value);

    QString cookieFile() const;
    void setCookieFile(const QString &cookieFile);

    bool diskCacheEnabled() const;
    void setDiskCacheEnabled(const bool value);

    bool ignoreSslErrors() const;
    void setIgnoreSslErrors(const bool value);

    bool localAccessRemote() const;
    void setLocalAccessRemote(const bool value);

    QString outputEncoding() const;
    void setOutputEncoding(const QString &value);

    bool pluginsEnabled() const;
    void setPluginsEnabled(const bool value);

    QString proxy() const;
    void setProxy(const QString &value);
    QString proxyHost() const;
    int proxyPort() const;

    QString auth() const;
    void setAuth(const QString &value);
    QString authUser() const;
    QString authPass() const;

    QStringList scriptArgs() const;
    void setScriptArgs(const QStringList &value);

    QString scriptEncoding() const;
    void setScriptEncoding(const QString &value);

    QString scriptFile() const;
    void setScriptFile(const QString &value);

    QString unknownOption() const;
    void setUnknownOption(const QString &value);

    bool versionFlag() const;
    void setVersionFlag(const bool value);

private:
    void resetToDefaults();
    void setProxyHost(const QString &value);
    void setProxyPort(const int value);
    void setAuthUser(const QString &value);
    void setAuthPass(const QString &value);

    bool m_autoLoadImages;
    QString m_cookieFile;
    bool m_diskCacheEnabled;
    bool m_ignoreSslErrors;
    bool m_localAccessRemote;
    QString m_outputEncoding;
    bool m_pluginsEnabled;
    QString m_proxyHost;
    int m_proxyPort;
    QStringList m_scriptArgs;
    QString m_scriptEncoding;
    QString m_scriptFile;
    QString m_unknownOption;
    bool m_versionFlag;
    QString m_authUser;
    QString m_authPass;

private:
    static QString normalisePath(const QString &path);
    static bool readFile(const QString &path, QString *const content);
};

#endif // CONFIG_H
